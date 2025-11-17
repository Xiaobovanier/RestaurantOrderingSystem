# 🍽️ Restaurant Ordering System (Python + PyQt6)

This project is a complete **Restaurant Ordering Application** developed as part of the **Software Development Attestation** program at **Vanier College**.  
It includes a full **desktop GUI**, **database layer**, **repository modules**, and a complete **Phase III SDLC documentation**.

---

## 🚀 Features

### ✔️ GUI (PyQt6)
- Customer Management  
- Menu Item Management  
- Order Creation & Editing  
- Payment Processing  
- Daily Sales Reports  
- Manager Order Search  
- Clean themed interface with multiple windows

### ✔️ Back-End
- MySQL database integration  
- Repository pattern for CRUD  
- Modular code structure  
- Models for all business entities  
- Utilities for calculation (tax, subtotal, total)

---

## 📁 Project Structure

RestaurantOrderingSystem/
│
├── docs/ # SDLC Report
│ └── Restaurant_Ordering_Application_Phase_III_Xiaobo_Zhan.docx
│
├── src/ # Application source code
│ ├── app.py # Main entry point
│ ├── models.py # Data models
│ ├── db.py # Database connection
│ ├── db_config.py # DB settings
│ ├── theme.py # App theme
│ ├── calc.py # Calculation utilities
│ │
│ ├── customers_repo.py # CRUD Repositories
│ ├── menu_repo.py
│ ├── orders_repo.py
│ ├── payments_repo.py
│ │
│ ├── customer_window.py # GUI Windows
│ ├── menu_window.py
│ ├── order_window.py
│ ├── daily_report_window.py
│ ├── order_search_window.py
│ ├── payment_history_window.py
│
└── .gitignore


---

## 🗂️ SDLC Documentation

This repository includes a complete **Phase III SDLC Report**, covering:

- System Planning  
- System Analysis  
- System Design  
- Use Case Diagram  
- Class Diagram  
- ERD  
- Sequence Diagram  
- DFD / FDD  
- Implementation & Testing  
- Conclusions  

📄 Located in:  
/docs/Restaurant_Ordering_Application


---

## ▶️ How to Run

### 1. Install dependencies  
pip install PyQt6 mysql-connector-python

### 2. Configure database  
Edit:
src/db_config.py

### 3. Run application  
python src/app.py


---

## 👨‍🎓 Author

**Xiaobo Zhan**  
Software Development Attestation  
Vanier College, Montreal
