import contextvars
import json
from pydantic import BaseModel, Field
import agent.config_data as config
from agent.sqlalchemy_history_store import get_history
from database.models import Product
from database.session import SessionLocal
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from module_order.order_service import create_order_data, serialize_order
from module_order.order_vo import OrderCreate, OrderItemCreate, PrepareOrderMultipleProducts
from sqlalchemy import select, and_
from typing import Annotated

SYSTEM_PROMPT = """你是智能买手，帮助用户查询商品并代购下单。
流程：
1. 用 list_products 查商品，记住返回的 product_id。
2. 用户表达购买意图时，必须调用 prepare_order，使用 list_products 中的 product_id 和对应数量，不要只用文字回复。
3. 如果调用prepare_order查到的某些商品库存不足时，使用 search_similar_products 搜索相似产品，并提示用户是否购买；如果用户同意，则调用 重新走到流程第二步，如果用户不同意，则提示用户并结束流程。
4. 只有用户在下一轮对话中明确表示「确认」「好的」「下单」等时，才调用 confirm_order 真正下单。
5. 禁止在同一轮对话里连续调用 prepare_order 和 confirm_order。"""

_pending_orders: dict[str, dict] = {}
_session_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "product_agent_session_id", default=None
)


def _current_session_id() -> str:
    session_id = _session_id_ctx.get()
    if session_id is None:
        raise RuntimeError("session_id 未设置")
    return session_id


@tool
def list_products() -> str:
    """列出所有可购商品，返回 id、名称、价格。"""
    with SessionLocal() as db:
        products = db.scalars(select(Product).where(Product.balance > 0).order_by(Product.id)).all()
        data = [{"id": p.id, "name": p.name, "price": p.price, "balance": p.balance} for p in products]
    return json.dumps(data, ensure_ascii=False)

def _get_product_str(products: list[Product]) -> str:
    return ", ".join([f"产品id:{p.id}, 名字:{p.name} 数量:{p.quantity}" for p in products])

# def prepare_order(items: PrepareOrderMultipleProducts) -> str:
# def prepare_order(product_id: int, quantity: int, remark: str | None = None) -> str:

@tool
def prepare_order(items: PrepareOrderMultipleProducts) -> str:
    """生成待确认订单，不真正下单。用户确认后再调用 confirm_order。"""
    # for product in items.products:
    #     print(f"product_id: {product.product_id}, quantity: {product.quantity}")
    with SessionLocal() as db:
        stmt = select(Product).where(and_(Product.id.in_(item.product_id for item in items.products), Product.balance > 0))
        products = db.scalars(stmt).all()

        product_map = {product.id: product for product in products}
        total_price = 0
        draft = []

        missing = []
        insufficient = []
        for product in items.products:
            # 找出缺失的商品
            if product.product_id not in product_map:
                missing.append(product)
            # 找出库存不足的商品
            elif product_map[product.product_id].balance < product.quantity:
                insufficient.append(product)

            draft.append({
                "product_id": product.product_id,
                "product_name": product_map[product.product_id].name,
                "quantity": product.quantity,
                "price": product_map[product.product_id].price,
            })
            total_price += product_map[product.product_id].price * product.quantity

        if len(missing) > 0 or len(insufficient) > 0:
            print(f"------missing_product: {missing}")
            print(f"------insufficient_product: {insufficient}")
            # return json.dumps({"error": f"部分商品不存在, 具体如下: {', '.join(missing_product_str)}"}, ensure_ascii=False)
            return json.dumps({
                "error": "部分商品缺货，无法下单",
                "missing": _get_product_str(missing),
                "insufficient": _get_product_str(insufficient)
            }, ensure_ascii=False)
        
        _pending_orders[_current_session_id()] = {
            "items": draft,
            "remark": items.remark or "",
        }
        msg_item = [f"{i['product_name']} x{i['quantity']}，单价 {i['price']}" for i in draft]
        resp = {
            "status": "pending_confirmation",
            "summary": {"items": draft, "total_price": total_price, "remark": items.remark},
            "message": f"请确认： {', '.join(msg_item)}，合计 {total_price}。回复「确认」后下单。",
        }

        return json.dumps(resp, ensure_ascii=False)

@tool
def search_similar_products(query: str) -> str:
    """搜索相似产品，返回产品id、名称、价格。"""
    with SessionLocal() as db:
        products = db.scalars(select(Product).where(Product.name.like(f"%{query}%")).order_by(Product.id)).all()
        data = [{"id": p.id, "name": p.name, "price": p.price, "balance": p.balance} for p in products]
    return json.dumps(data, ensure_ascii=False)


@tool
def confirm_order() -> str:
    """用户确认后，根据待确认订单真正创建订单。"""
    session_id = _current_session_id()
    draft = _pending_orders.get(session_id)
    if draft is None:
        return json.dumps({"error": "没有待确认订单，请先 prepare_order"}, ensure_ascii=False)

    with SessionLocal() as db:
        order = create_order_data(
            OrderCreate(
                items=[
                    OrderItemCreate(
                        product_id=draft_item["product_id"],
                        quantity=draft_item["quantity"],
                        price=draft_item["price"],
                    )
                    for draft_item in draft["items"]
                ],
                remark=draft.get("remark", ""),
            ),
            db,
        )
        result = serialize_order(order)

    del _pending_orders[session_id]
    return json.dumps(result, ensure_ascii=False, default=str)


PRODUCT_TOOLS = [list_products, prepare_order, confirm_order, search_similar_products]
_TOOL_MAP = {t.name: t for t in PRODUCT_TOOLS}


def run_product_agent(question: str, session_id: str) -> str:
    session_token = _session_id_ctx.set(session_id)
    prepared_this_turn = False
    try:
        history = get_history(session_id)
        human_msg = HumanMessage(content=question)
        turn_messages: list[BaseMessage] = [human_msg]
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *history.messages,
            human_msg,
        ]
        llm = ChatTongyi(model=config.chat_model_name).bind_tools(PRODUCT_TOOLS)

        for _ in range(5):
            ai_msg = llm.invoke(messages)
            turn_messages.append(ai_msg)
            if not ai_msg.tool_calls:
                history.add_messages(turn_messages)
                return ai_msg.content or "已完成。"

            messages.append(ai_msg)
            for tc in ai_msg.tool_calls:
                if tc["name"] == "confirm_order" and prepared_this_turn:
                    result = json.dumps(
                        {"error": "请等待用户在下一条消息中确认后再下单"},
                        ensure_ascii=False,
                    )
                else:
                    tool_fn = _TOOL_MAP[tc["name"]]
                    result = tool_fn.invoke(tc["args"])
                    if tc["name"] == "prepare_order":
                        prepared_this_turn = True
                tool_msg = ToolMessage(content=str(result), tool_call_id=tc["id"], name=tc["name"])
                messages.append(tool_msg)
                turn_messages.append(tool_msg)
    finally:
        _session_id_ctx.reset(session_token)

    return "处理超时，请重试。"
