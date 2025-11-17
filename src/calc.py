
STATE_TAX = 0.05
LOCAL_TAX = 0.09975

def calculate_item_total(price: float, qty: int) -> float:
    return round(price * qty, 2)

def calculate_order_total(order_items: dict, menu: dict) -> float:
    total = 0.0
    for item_id, qty in order_items.items():
        if item_id not in menu:
            continue
        price = float(menu[item_id]["price"]) if isinstance(menu[item_id], dict) else float(menu[item_id][1])
        total += calculate_item_total(price, int(qty))
    return round(total, 2)

def total_with_tax(subtotal: float) -> tuple[float, float, float]:
    st = round(subtotal * STATE_TAX, 2)
    lt = round(subtotal * LOCAL_TAX, 2)
    return st, lt, round(subtotal + st + lt, 2)
