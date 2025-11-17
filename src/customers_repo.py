
from models import Customer
from db import query, execute, execute_returning_id

def list_customers() -> list[Customer]:
    rows = query("SELECT customer_id, name, phone, address, password FROM customers ORDER BY customer_id")
    return [Customer(**r) for r in rows]

def add_customer(name: str, phone: str, addr: str, pwd: str = '') -> Customer:
    new_id = execute_returning_id(
        "INSERT INTO customers(name, phone, address, password) VALUES (%s,%s,%s,%s)",
        (name, phone, addr, pwd)
    )
    return Customer(new_id, name, phone, addr, pwd)

def update_customer(c: Customer) -> None:
    execute("UPDATE customers SET name=%s, phone=%s, address=%s, password=%s WHERE customer_id=%s",
            (c.name, c.phone, c.address, c.password, c.customer_id))

def delete_customer(customer_id: int) -> None:
    execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
