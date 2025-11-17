
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDateEdit, QComboBox
from PyQt6.QtCore import QDate
from orders_repo import daily_summary

class DailyReportWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Daily Report (DB)')

        self.date = QDateEdit(); self.date.setCalendarPopup(True); self.date.setDate(QDate.currentDate())
        self.cmb_status = QComboBox(); self.cmb_status.addItems(['', 'Accepted', 'Delivered', 'Cancelled'])
        self.cust = QLineEdit(); self.cust.setPlaceholderText("Customer ID (Optional)")
        self.btn = QPushButton('Generate')

        top = QHBoxLayout()
        top.addWidget(QLabel('Date:')); top.addWidget(self.date)
        top.addWidget(QLabel('Status:')); top.addWidget(self.cmb_status)
        top.addWidget(QLabel('Customer:')); top.addWidget(self.cust)
        top.addWidget(self.btn)

        self.text = QTextEdit(); self.text.setReadOnly(True)

        layout = QVBoxLayout(); layout.addLayout(top); layout.addWidget(self.text)
        self.setLayout(layout)

        self.btn.clicked.connect(self.generate)

    def generate(self):
        date_str = self.date.date().toString('yyyy-MM-dd')
        status = self.cmb_status.currentText().strip() or None
        cust_id = int(self.cust.text()) if self.cust.text().strip().isdigit() else None

        head, by_status, top_items = daily_summary(date_str, cust_id, status)
        lines=[]
        lines.append(f"Date: {date_str}")
        lines.append(f"Total Orders: {head['cnt']}")
        lines.append(f"Total Revenue: {float(head['revenue']):.2f}")
        lines.append(f"Avg Ticket: {float(head['avg_ticket']):.2f}")
        lines.append("\nBy Status:")
        for r in by_status:
            lines.append(f"  {r['status']}: {r['n']}")
        lines.append("\nTop Items:")
        for r in top_items:
            lines.append(f"  {r['item_id']} - {r['name']}: {r['qty_sum']}")
        self.text.setPlainText("\n".join(lines))
