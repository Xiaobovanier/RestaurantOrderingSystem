
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QSpinBox, QPushButton, QMessageBox
from customers_repo import list_customers
from menu_repo import list_items
from orders_repo import add_order, update_order_status
from payments_repo import add_payment
from models import Order, Payment
from calc import calculate_order_total, total_with_tax

class OrderWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Orders & Payment')

        self.cmb_customer = QComboBox()
        for c in list_customers():
            self.cmb_customer.addItem(f"{c.customer_id} - {c.name}", c.customer_id)

        self.menu = list_items()
        self.table = QTableWidget(len(self.menu), 3)
        self.table.setHorizontalHeaderLabels(['Item', 'Price', 'Qty'])
        for r, m in enumerate(self.menu):
            self.table.setItem(r, 0, QTableWidgetItem(f"{m.item_id} - {m.name}"))
            self.table.setItem(r, 1, QTableWidgetItem(f"{m.price:.2f}"))
            sb = QSpinBox(); sb.setRange(0, 20); self.table.setCellWidget(r, 2, sb)

        self.lbl_sub = QLabel('Subtotal: 0.00')
        self.lbl_tax = QLabel('Taxes: 0.00')
        self.lbl_tot = QLabel('Total: 0.00')

        self.btn_calc = QPushButton('Calculate')
        self.btn_save = QPushButton('Save Order')
        self.btn_pay = QPushButton('Process Payment')
        self.btn_status = QPushButton('Mark Delivered')

        top = QHBoxLayout(); top.addWidget(QLabel('Customer:')); top.addWidget(self.cmb_customer)
        totals = QHBoxLayout(); totals.addWidget(self.lbl_sub); totals.addWidget(self.lbl_tax); totals.addWidget(self.lbl_tot)
        btns = QHBoxLayout(); btns.addWidget(self.btn_calc); btns.addWidget(self.btn_save); btns.addWidget(self.btn_pay); btns.addWidget(self.btn_status)

        layout = QVBoxLayout(); layout.addLayout(top); layout.addWidget(self.table); layout.addLayout(totals); layout.addLayout(btns)
        self.setLayout(layout)

        self.btn_calc.clicked.connect(self.on_calc)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_pay.clicked.connect(self.on_pay)
        self.btn_status.clicked.connect(self.on_status)

        self._last_order_id = 0
        self._last_total = 0.0

    def collect_items(self) -> dict:
        items = {}
        for r, m in enumerate(self.menu):
            sb = self.table.cellWidget(r, 2)
            qty = int(sb.value())
            if qty > 0:
                items[m.item_id] = qty
        return items

    def on_calc(self):
        items = self.collect_items()
        if not items:
            QMessageBox.information(self, 'Info', 'Select at least one item'); return
        menu_map = {m.item_id: {"name": m.name, "price": m.price} for m in self.menu}
        subtotal = calculate_order_total(items, menu_map)
        st, lt, total = total_with_tax(subtotal)
        self.lbl_sub.setText(f'Subtotal: {subtotal:.2f}')
        self.lbl_tax.setText(f'Taxes: {(st+lt):.2f}')
        self.lbl_tot.setText(f'Total: {total:.2f}')
        self._last_total = total

    def on_save(self):
        items = self.collect_items()
        if not items:
            QMessageBox.warning(self, 'Validation', 'No items selected'); return
        menu_map = {m.item_id: {"name": m.name, "price": m.price} for m in self.menu}
        subtotal = calculate_order_total(items, menu_map)
        st, lt, total = total_with_tax(subtotal)
        order = Order(0, int(self.cmb_customer.currentData()), items, subtotal, st, lt, total, 'Accepted')
        saved = add_order(order)
        self._last_order_id = saved.order_id
        self._last_total = total
        QMessageBox.information(self, 'Saved', f'Order #{saved.order_id} saved. Total {total:.2f}')

    def on_pay(self):
        if self._last_order_id == 0:
            QMessageBox.warning(self, 'Validation', 'Save the order first'); return
        pid = f"P{self._last_order_id}001"; txn = f"T{self._last_order_id}001"
        p = Payment(pid, self._last_order_id, 'Debit Card', float(self._last_total), 'Paid', txn)
        add_payment(p)
        QMessageBox.information(self, 'Paid', f'Payment {pid} completed')

    def on_status(self):
        if self._last_order_id == 0:
            QMessageBox.warning(self, 'Validation', 'No order selected'); return
        update_order_status(self._last_order_id, 'Delivered')
        QMessageBox.information(self, 'Status', f'Order #{self._last_order_id} marked Delivered')
