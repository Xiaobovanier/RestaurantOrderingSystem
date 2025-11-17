from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QWidget, QVBoxLayout, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QRect

from customer_window import CustomerWindow
from menu_window import MenuWindow
from order_window import OrderWindow
from daily_report_window import DailyReportWindow
from order_search_window import OrderSearchWindow
from payment_history_window import PaymentHistoryWindow


_open_windows = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Restaurant Ordering – Main')
        self.resize(550, 550)
        self.setMinimumSize(430, 500)

        #Buttons
        btn_width = 220
        btn_height = 42

        self.btn_customers = QPushButton('Customers')
        self.btn_customers.setFixedSize(btn_width, btn_height)

        self.btn_menu = QPushButton('Menu')
        self.btn_menu.setFixedSize(btn_width, btn_height)

        self.btn_orders = QPushButton('Orders  Payment')
        self.btn_orders.setFixedSize(btn_width, btn_height)

        self.btn_reports = QPushButton('Daily Report')
        self.btn_reports.setFixedSize(btn_width, btn_height)

        self.btn_mgr_search = QPushButton('Manager: Search Orders')
        self.btn_mgr_search.setFixedSize(btn_width, btn_height)

        self.btn_pay_hist = QPushButton('Payment History')
        self.btn_pay_hist.setFixedSize(btn_width, btn_height)

        #Layout
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(70, 60, 70, 60)

        layout.addStretch()
        for b in [
            self.btn_customers, self.btn_menu, self.btn_orders,
            self.btn_reports, self.btn_mgr_search, self.btn_pay_hist
        ]:
            layout.addWidget(b, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStatusBar(QStatusBar())


        self.btn_customers.clicked.connect(lambda: self.open_window(CustomerWindow))
        self.btn_menu.clicked.connect(lambda: self.open_window(MenuWindow))
        self.btn_orders.clicked.connect(lambda: self.open_window(OrderWindow))
        self.btn_reports.clicked.connect(lambda: self.open_window(DailyReportWindow))
        self.btn_mgr_search.clicked.connect(lambda: self.open_window(OrderSearchWindow))
        self.btn_pay_hist.clicked.connect(lambda: self.open_window(PaymentHistoryWindow))

    def open_window(self, window_class):
        try:
            win = window_class()
            _open_windows.append(win)
            win.setWindowFlag(Qt.WindowType.Window, True)
            win.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.center_window(win)
            win.show()
            win.raise_()
            win.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open window:\n{e}")

    def center_window(self, win):
        main_geo: QRect = self.geometry()
        if main_geo.width() == 0:
            main_geo = QRect(300, 300, 800, 600)
        x = main_geo.x() + (main_geo.width() - 600) // 2
        y = main_geo.y() + (main_geo.height() - 400) // 2
        win.resize(700, 460)
        win.move(max(x, 100), max(y, 100))
        QTimer.singleShot(100, lambda: (win.raise_(), win.activateWindow()))
