
from models import MenuItem
from db import query, execute, execute_returning_id

def list_items() -> list[MenuItem]:
    rows = query("SELECT item_id, name, price, available FROM menu_items ORDER BY item_id")
    return [MenuItem(r['item_id'], r['name'], float(r['price']), bool(r['available'])) for r in rows]

def add_item(name: str, price: float, available: bool = True) -> MenuItem:
    new_id = execute_returning_id(
        "INSERT INTO menu_items(name, price, available) VALUES (%s,%s,%s)",
        (name, price, 1 if available else 0)
    )
    return MenuItem(new_id, name, float(price), available)

def update_item(m: MenuItem) -> None:
    execute("UPDATE menu_items SET name=%s, price=%s, available=%s WHERE item_id=%s",
            (m.name, m.price, 1 if m.available else 0, m.item_id))

def delete_item(item_id: int) -> None:
    execute("DELETE FROM menu_items WHERE item_id=%s", (item_id,))
