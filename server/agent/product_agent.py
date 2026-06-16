import json

import agent.config_data as config
from agent.sqlalchemy_history_store import get_history
from database.models import Product
from database.session import SessionLocal
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from module_order.order_service import create_order_data, serialize_order
from module_order.order_vo import OrderCreate, OrderItemCreate
from sqlalchemy import select

SYSTEM_PROMPT = """你是智能买手，帮助用户查询商品并代购下单。
流程：先用 list_products 查商品，用户明确要买时用 create_order 下单，然后告知订单结果。"""


@tool
def list_products() -> str:
    """列出所有可购商品，返回 id、名称、价格。"""
    with SessionLocal() as db:
        products = db.scalars(select(Product).order_by(Product.id)).all()
        data = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    return json.dumps(data, ensure_ascii=False)


@tool
def create_order(product_id: int, quantity: int, remark: str = "") -> str:
    """创建订单。product_id 为商品 ID，quantity 为购买数量。"""
    with SessionLocal() as db:
        product = db.get(Product, product_id)
        if product is None:
            return json.dumps({"error": "商品不存在"}, ensure_ascii=False)
        order = create_order_data(
            OrderCreate(
                items=[
                    OrderItemCreate(
                        product_id=product_id,
                        quantity=quantity,
                        price=product.price,
                    )
                ],
                remark=remark,
            ),
            db,
        )
        return json.dumps(serialize_order(order), ensure_ascii=False, default=str)


PRODUCT_TOOLS = [list_products, create_order]
_TOOL_MAP = {t.name: t for t in PRODUCT_TOOLS}


def run_product_agent(question: str, session_id: str) -> str:
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
            tool_fn = _TOOL_MAP[tc["name"]]
            result = tool_fn.invoke(tc["args"])
            messages.append(
                ToolMessage(content=str(result), tool_call_id=tc["id"])
            )

    return "处理超时，请重试。"
