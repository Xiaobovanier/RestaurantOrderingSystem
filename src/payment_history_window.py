from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit
)
from payments_repo import list_payments_by_order, list_payments_by_customer, list_paid_orders


class PaymentHistoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Payment History')

        # --- Search controls ---
        self.ed_order = QLineEdit();
        self.ed_order.setPlaceholderText("Order ID")
        self.btn_order = QPushButton('Search by Order')

        self.ed_customer = QLineEdit();
        self.ed_customer.setPlaceholderText("Customer ID")
        self.btn_customer = QPushButton('Search by Customer')

        self.btn_summary = QPushButton("Order Summary")
        self.text_summary = QTextEdit()
        self.text_summary.setReadOnly(True)


        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Order:"));
        row1.addWidget(self.ed_order);
        row1.addWidget(self.btn_order)
        row1.addWidget(QLabel("Customer:"));
        row1.addWidget(self.ed_customer);
        row1.addWidget(self.btn_customer)

        # --- Second Row (Order Summary) ---
        row2 = QHBoxLayout()
        self.btn_summary.setFixedWidth(140)
        row2.addStretch()
        row2.addWidget(self.btn_summary)
        row2.addStretch() 

        # --- Table ---
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(['PaymentID', 'OrderID', 'Method', 'Amount', 'Status', 'TxnID', 'PaidAt'])

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Paid Order Summary:"))
        layout.addWidget(self.text_summary)
        self.setLayout(layout)


        self.btn_order.clicked.connect(self.search_order)
        self.btn_customer.clicked.connect(self.search_customer)
        self.btn_summary.clicked.connect(self.show_summary)


    def _fill(self, rows):
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount();
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(r.get('payment_id'))))
            self.table.setItem(i, 1, QTableWidgetItem(str(r.get('order_id'))))
            self.table.setItem(i, 2, QTableWidgetItem(r.get('method', '')))
            self.table.setItem(i, 3, QTableWidgetItem(f"{float(r.get('amount', 0)):.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(r.get('status', '')))
            self.table.setItem(i, 5, QTableWidgetItem(r.get('transaction_id', '')))
            self.table.setItem(i, 6, QTableWidgetItem(r.get('paid_at', '')))

    def search_order(self):
        if not self.ed_order.text().isdigit():
            return
        rows = list_payments_by_order(int(self.ed_order.text()))
        self._fill(rows)

    def search_customer(self):
        if not self.ed_customer.text().isdigit():
            return
        rows = list_payments_by_customer(int(self.ed_customer.text()))
        self._fill(rows)


    def show_summary(self):
        rows = list_paid_orders()
        if not rows:
            self.text_summary.setPlainText("No paid orders found.")
            return

        lines = []
        for r in rows:
            lines.append(
                f"Order #{r['order_id']} | Customer: {r['customer_id']} | Total: {r['total']:.2f} | "
                f"Payment: {r['payment_id']} ({r['method']}) | Txn {r['transaction_id']} | Paid at {r['paid_at']}"
            )
        self.text_summary.setPlainText("\n".join(lines))
