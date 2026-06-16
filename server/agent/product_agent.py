import contextvars
import json
from pydantic import BaseModel, Field
import agent.config_data as config
from agent.sqlalchemy_history_store import get_history
from database.models import Product
from database.session import SessionLocal
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from module_order.order_service import create_order_data, serialize_order
from module_order.order_vo import OrderCreate, OrderItemCreate, PrepareOrderMultipleProducts
from sqlalchemy import select, and_
from typing import Annotated

SYSTEM_PROMPT = """你是智能买手，帮助用户查询商品并代购下单。
流程：
1. 用 list_products 查商品。
2. 用户表达购买意图时，调用 prepare_order 生成待确认订单，并向用户展示摘要，请其确认。
3. 只有用户在下一轮对话中明确表示「确认」「好的」「下单」等时，才调用 confirm_order 真正下单。
4. 禁止在同一轮对话里连续调用 prepare_order 和 confirm_order。"""

_pending_orders: dict[str, list[dict]] = {}
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
        if len(products) != len(items.products):
            return json.dumps({"error": "部分商品不存在"}, ensure_ascii=False)

        product_map = {product.id: product for product in products}
        total_price = 0
        draft = []
        for product in items.products:
            draft.append({
                "product_id": product.product_id,
                "product_name": product_map[product.product_id].name,
                "quantity": product.quantity,
                "price": product_map[product.product_id].price,
            })
            total_price += product_map[product.product_id].price * product.quantity
        
        _pending_orders[_current_session_id()] = draft
        msg_item = [f"{i['product_name']} x{i['quantity']}，单价 {i['price']}" for i in draft]
        resp = {
            "status": "pending_confirmation",
            "summary": items.model_dump(),
            "message": f"请确认： {', '.join(msg_item)}，合计 {total_price}。回复「确认」后下单。",
        }

        return json.dumps(resp, ensure_ascii=False)


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
                    ) for draft_item in draft
                ],
                remark=draft.get("remark", ""),
            ),
            db,
        )
        result = serialize_order(order)

    del _pending_orders[session_id]
    return json.dumps(result, ensure_ascii=False, default=str)


PRODUCT_TOOLS = [list_products, prepare_order, confirm_order]
_TOOL_MAP = {t.name: t for t in PRODUCT_TOOLS}


def run_product_agent(question: str, session_id: str) -> str:
    session_token = _session_id_ctx.set(session_id)
    prepared_this_turn = False
    try:
        history = get_history(session_id)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *history.messages,
            HumanMessage(content=question),
        ]
        llm = ChatTongyi(model=config.chat_model_name).bind_tools(PRODUCT_TOOLS)

        for _ in range(5):
            ai_msg = llm.invoke(messages)
            if not ai_msg.tool_calls:
                history.add_messages([HumanMessage(content=question), ai_msg])
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
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=tc["id"])
                )
    finally:
        _session_id_ctx.reset(session_token)

    return "处理超时，请重试。"
