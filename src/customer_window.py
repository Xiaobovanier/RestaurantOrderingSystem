from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel, QMessageBox
from customers_repo import list_customers, add_customer, update_customer, delete_customer
from models import Customer


class CustomerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Customers')


        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Phone', 'Address'])


        self.name = QLineEdit(); self.phone = QLineEdit(); self.addr = QLineEdit()
        self.btn_add = QPushButton('Add'); self.btn_update = QPushButton('Update'); self.btn_delete = QPushButton('Delete')


        form = QHBoxLayout()
        form.addWidget(QLabel('Name:')); form.addWidget(self.name)
        form.addWidget(QLabel('Phone:')); form.addWidget(self.phone)
        form.addWidget(QLabel('Address:')); form.addWidget(self.addr)


        btns = QHBoxLayout(); btns.addWidget(self.btn_add); btns.addWidget(self.btn_update); btns.addWidget(self.btn_delete)


        layout = QVBoxLayout(); layout.addWidget(self.table); layout.addLayout(form); layout.addLayout(btns)
        self.setLayout(layout)

        self.btn_add.clicked.connect(self.on_add)
        self.btn_update.clicked.connect(self.on_update)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellClicked.connect(self.on_select)

        self.refresh()


    def refresh(self):
        data = list_customers()
        self.table.setRowCount(0)
        for c in data:
            r = self.table.rowCount(); self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(c.customer_id)))
            self.table.setItem(r, 1, QTableWidgetItem(c.name))
            self.table.setItem(r, 2, QTableWidgetItem(c.phone))
            self.table.setItem(r, 3, QTableWidgetItem(c.address))


    def on_add(self):
        if not self.name.text():
            QMessageBox.warning(self, 'Validation', 'Name is required'); return
        c = add_customer(self.name.text(), self.phone.text(), self.addr.text())
        self.refresh()


    def on_update(self):
        row = self.table.currentRow()
        if row < 0: return
        cid = int(self.table.item(row, 0).text())
        c = Customer(cid, self.name.text(), self.phone.text(), self.addr.text(), '')
        update_customer(c); self.refresh()


    def on_delete(self):
        row = self.table.currentRow()
        if row < 0: return
        cid = int(self.table.item(row, 0).text())
        delete_customer(cid); self.refresh()


    def on_select(self, row, col):
        self.name.setText(self.table.item(row,1).text())
        self.phone.setText(self.table.item(row,2).text())
        self.addr.setText(self.table.item(row,3).text())