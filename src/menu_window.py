from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel, QMessageBox, QCheckBox
from menu_repo import list_items, add_item, update_item, delete_item
from models import MenuItem


class MenuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Menu Items')


        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Price', 'Available'])


        self.name = QLineEdit(); self.price = QLineEdit(); self.available = QCheckBox('Available')
        self.available.setChecked(True)
        self.btn_add = QPushButton('Add'); self.btn_update = QPushButton('Update'); self.btn_delete = QPushButton('Delete')


        form = QHBoxLayout()
        form.addWidget(QLabel('Name:')); form.addWidget(self.name)
        form.addWidget(QLabel('Price:')); form.addWidget(self.price)
        form.addWidget(self.available)


        btns = QHBoxLayout(); btns.addWidget(self.btn_add); btns.addWidget(self.btn_update); btns.addWidget(self.btn_delete)


        layout = QVBoxLayout(); layout.addWidget(self.table); layout.addLayout(form); layout.addLayout(btns)
        self.setLayout(layout)


        self.btn_add.clicked.connect(self.on_add)
        self.btn_update.clicked.connect(self.on_update)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellClicked.connect(self.on_select)

        self.refresh()


    def refresh(self):
        data = list_items(); self.table.setRowCount(0)
        for m in data:
            r = self.table.rowCount(); self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(m.item_id)))
            self.table.setItem(r, 1, QTableWidgetItem(m.name))
            self.table.setItem(r, 2, QTableWidgetItem(f"{m.price:.2f}"))
            self.table.setItem(r, 3, QTableWidgetItem('Yes' if m.available else 'No'))


    def on_add(self):
        try:
            price = float(self.price.text())
        except Exception:
            QMessageBox.warning(self, 'Validation', 'Price must be a number'); return
        add_item(self.name.text(), price, self.available.isChecked()); self.refresh()


    def on_update(self):
        row = self.table.currentRow()
        if row < 0:
            return
        iid = int(self.table.item(row, 0).text())
        try:
            price = float(self.price.text())
        except Exception:
            QMessageBox.warning(self, 'Validation', 'Price must be a number')
            return
        m = MenuItem(iid, self.name.text(), price, self.available.isChecked())
        update_item(m)
        self.refresh()


    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            return
        iid = int(self.table.item(row, 0).text())
        delete_item(iid)
        self.refresh()


    def on_select(self, row, col):
        self.name.setText(self.table.item(row,1).text())
        self.price.setText(self.table.item(row,2).text())
        self.available.setChecked(self.table.item(row,3).text().lower().startswith('y'))