
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox
from PyQt6.QtCore import QDate
from orders_repo import search_orders

class OrderSearchWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Manager – Search Orders')

        self.ed_order = QLineEdit(); self.ed_order.setPlaceholderText("Order ID")
        self.ed_customer = QLineEdit(); self.ed_customer.setPlaceholderText("Customer ID")
        self.dt_from = QDateEdit(); self.dt_from.setCalendarPopup(True); self.dt_from.setDate(QDate.currentDate())
        self.dt_to   = QDateEdit(); self.dt_to.setCalendarPopup(True); self.dt_to.setDate(QDate.currentDate())
        self.cmb_status = QComboBox(); self.cmb_status.addItems(['', 'Accepted', 'Delivered', 'Cancelled'])
        self.btn = QPushButton("Search")

        top = QHBoxLayout()
        top.addWidget(QLabel("Order:")); top.addWidget(self.ed_order)
        top.addWidget(QLabel("Customer:")); top.addWidget(self.ed_customer)
        top.addWidget(QLabel("From:")); top.addWidget(self.dt_from)
        top.addWidget(QLabel("To:")); top.addWidget(self.dt_to)
        top.addWidget(QLabel("Status:")); top.addWidget(self.cmb_status)
        top.addWidget(self.btn)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(['OrderID','Customer','Subtotal','Taxes','Total','Status','Created'])

        layout = QVBoxLayout(); layout.addLayout(top); layout.addWidget(self.table)
        self.setLayout(layout)

        self.btn.clicked.connect(self.do_search)

    def do_search(self):
        order_id = int(self.ed_order.text()) if self.ed_order.text().isdigit() else None
        customer = int(self.ed_customer.text()) if self.ed_customer.text().isdigit() else None
        date_from = self.dt_from.date().toString('yyyy-MM-dd')
        date_to   = self.dt_to.date().toString('yyyy-MM-dd')
        status = self.cmb_status.currentText().strip() or None

        rows = search_orders(order_id, customer, date_from, date_to, status)
        self.table.setRowCount(0)
        for o in rows:
            r = self.table.rowCount(); self.table.insertRow(r)
            taxes = o.state_tax + o.local_tax
            self.table.setItem(r, 0, QTableWidgetItem(str(o.order_id)))
            self.table.setItem(r, 1, QTableWidgetItem(str(o.customer_id)))
            self.table.setItem(r, 2, QTableWidgetItem(f"{o.subtotal:.2f}"))
            self.table.setItem(r, 3, QTableWidgetItem(f"{taxes:.2f}"))
            self.table.setItem(r, 4, QTableWidgetItem(f"{o.total:.2f}"))
            self.table.setItem(r, 5, QTableWidgetItem(o.status))
            self.table.setItem(r, 6, QTableWidgetItem(o.created_at))
