
from models import Payment
from db import execute, query


def add_payment(p: Payment) -> Payment:
    execute("""
        INSERT INTO payments(payment_id, order_id, method, amount, status, transaction_id, paid_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (p.payment_id, p.order_id, p.method, p.amount, p.status, p.transaction_id, p.paid_at))
    return p


def list_payments_by_order(order_id: int):
    return query("""
        SELECT 
            payment_id,
            order_id,
            method,
            amount,
            status,
            transaction_id,
            DATE_FORMAT(paid_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS paid_at
        FROM payments
        WHERE order_id=%s
        ORDER BY paid_at DESC
    """, (order_id,))


def list_payments_by_customer(customer_id: int):
    return query("""
        SELECT 
            p.payment_id,
            p.order_id,
            o.customer_id,
            p.method,
            p.amount,
            p.status,
            p.transaction_id,
            DATE_FORMAT(p.paid_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS paid_at
        FROM payments p 
        JOIN orders o ON p.order_id=o.order_id
        WHERE o.customer_id=%s
        ORDER BY p.paid_at DESC
    """, (customer_id,))


# ✅ 新增：列出所有已付款订单汇总
def list_paid_orders():
    return query("""
        SELECT 
            o.order_id,
            o.customer_id,
            o.total,
            p.payment_id,
            p.method,
            p.transaction_id,
            DATE_FORMAT(p.paid_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS paid_at
        FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        WHERE p.status='Paid'
        ORDER BY p.paid_at DESC
    """)


