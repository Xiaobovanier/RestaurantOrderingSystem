
from typing import List, Dict
from models import Order
from db import query, execute, execute_returning_id


def list_orders() -> List[Order]:
    rows = query("""
        SELECT 
            order_id, customer_id, subtotal, state_tax, local_tax, total, status,
            DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at
        FROM orders 
        ORDER BY order_id DESC
    """)

    res = []
    for r in rows:
        items = _get_order_items(r['order_id'])
        res.append(Order(
            order_id=r['order_id'], customer_id=r['customer_id'],
            items=items, subtotal=float(r['subtotal']),
            state_tax=float(r['state_tax']), local_tax=float(r['local_tax']),
            total=float(r['total']), status=r['status'], created_at=r['created_at']
        ))
    return res


def _get_order_items(order_id: int) -> Dict[int, int]:
    rows = query("SELECT item_id, qty FROM order_items WHERE order_id=%s", (order_id,))
    return {int(r['item_id']): int(r['qty']) for r in rows}


def add_order(order: Order) -> Order:
    new_id = execute_returning_id(
        "INSERT INTO orders(customer_id, subtotal, state_tax, local_tax, total, status) VALUES (%s,%s,%s,%s,%s,%s)",
        (order.customer_id, order.subtotal, order.state_tax, order.local_tax, order.total, order.status)
    )


    price_rows = query(
        "SELECT item_id, price FROM menu_items WHERE item_id IN (" +
        ",".join(["%s"] * len(order.items)) + ")",
        tuple(order.items.keys())
    )
    price_map = {int(r['item_id']): float(r['price']) for r in price_rows}

    params = []
    for item_id, qty in order.items.items():
        params.append((new_id, item_id, qty, price_map.get(item_id, 0.0)))

    if params:
        execute("INSERT INTO order_items(order_id, item_id, qty, price_at_order) VALUES (%s,%s,%s,%s)", params, many=True)

    order.order_id = new_id
    return order


def update_order_status(order_id: int, status: str) -> None:
    execute("UPDATE orders SET status=%s WHERE order_id=%s", (status, order_id))



def search_orders(order_id: int | None = None,
                  customer_id: int | None = None,
                  date_from: str | None = None,
                  date_to: str | None = None,
                  status: str | None = None) -> List[Order]:

    sql = """
        SELECT
            o.order_id,
            o.customer_id,
            o.subtotal,
            o.state_tax,
            o.local_tax,
            o.total,
            o.status,
            DATE_FORMAT(o.created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at
        FROM orders o
        WHERE 1=1
    """

    params = []

    if order_id:
        sql += " AND o.order_id = %s"
        params.append(order_id)

    if customer_id:
        sql += " AND o.customer_id = %s"
        params.append(customer_id)

    if date_from:
        sql += " AND DATE(o.created_at) >= DATE(%s)"
        params.append(date_from)

    if date_to:
        sql += " AND DATE(o.created_at) <= DATE(%s)"
        params.append(date_to)

    if status:
        sql += " AND o.status = %s"
        params.append(status)

    sql += " ORDER BY o.order_id DESC"

    rows = query(sql, params)

    res = []
    for r in rows:
        items = _get_order_items(r['order_id'])
        res.append(Order(
            r['order_id'], r['customer_id'], items,
            float(r['subtotal']), float(r['state_tax']), float(r['local_tax']),
            float(r['total']), r['status'], r['created_at']
        ))
    return res


def daily_summary(date_str: str | None = None, customer_id: int | None = None, status: str | None = None):

    sql = ["SELECT COUNT(*) AS cnt, COALESCE(SUM(total),0) AS revenue, COALESCE(AVG(total),0) AS avg_ticket",
           "FROM orders WHERE 1=1"]
    params = []
    if date_str:
        sql.append("AND DATE(created_at)=DATE(%s)"); params.append(date_str)
    if customer_id:
        sql.append("AND customer_id=%s"); params.append(customer_id)
    if status:
        sql.append("AND status=%s"); params.append(status)
    head = query(" ".join(sql), params)[0]

    sql2 = ["SELECT status, COUNT(*) AS n FROM orders WHERE 1=1"]
    params2 = []
    if date_str:
        sql2.append("AND DATE(created_at)=DATE(%s)"); params2.append(date_str)
    sql2.append("GROUP BY status")
    by_status = query(" ".join(sql2), params2)

    sql3 = ["SELECT oi.item_id, mi.name, SUM(oi.qty) AS qty_sum",
            "FROM order_items oi JOIN orders o ON oi.order_id=o.order_id",
            "JOIN menu_items mi ON oi.item_id=mi.item_id",
            "WHERE 1=1"]
    params3 = []
    if date_str:
        sql3.append("AND DATE(o.created_at)=DATE(%s)"); params3.append(date_str)
    sql3.append("GROUP BY oi.item_id, mi.name ORDER BY qty_sum DESC LIMIT 10")
    top_items = query(" ".join(sql3), params3)

    return head, by_status, top_items
