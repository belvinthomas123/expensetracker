# SpendWise - Elite Personal Expense Tracker

A high-performance, audit-ready financial ledger built with the Flask **Application Factory** pattern and **PostgreSQL**.

## 🌟 Elite Features
- **UUID Identifiers**: Uses secure, non-sequential UUIDs for all expenses to prevent data enumeration.
- **JSONB Audit Logs**: Track every single change (Insert, Update, Delete) with a full JSON history of old vs. new values.
- **Categorical Integrity**: Relational category system with automated seeding and custom brand-color accenting.
- **Premium Side-Bar UI**: A modern, responsive dashboard featuring **Plus Jakarta Sans** typography and a Ledger-style grouped transaction list.
- **Financial Precision**: Uses `NUMERIC(10,2)` for all currency fields to eliminate floating-point rounding errors.

---

## 🚀 Quick Start (Docker)
The most professional way to run this project:
```bash
docker-compose up --build
```
Access the dashboard at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🛠️ Architecture & Tradeoffs 

### 1. Modular Blueprint Design
Instead of a single-file script, I implemented a **Modular Factory Pattern**.
*   **Why?** This prevents circular imports, makes the app testable, and allows for adding "Admin" or "API" modules without refactoring the core.

### 2. JSONB Audit Trail
Every modification logs a record to the `expense_audit` table.
*   **Tradeoff**: It increases database storage slightly, but the benefit of data traceability and the ability to "Time Travel" through records is a mandatory production standard.

### 3. PostgreSQL Over SQLite
While the app has an SQLite fail-safe, the primary target is **PostgreSQL**.
*   **Why?** To utilize advanced types like `UUID` and `JSONB` which are not natively robust in SQLite, and to demonstrate proficiency with enterprise-grade RDBMS.

### 4. Custom Design System
Built with **Vanilla CSS Variables** instead of a cookie-cutter framework like Bootstrap.
*   **Why?** To demonstrate full control over the UI bundle size and a deep understanding of modern CSS architecture (Tokens, Components, Layouts).

---

## 📂 Project Structure
```text
├── app.py           # Application Factory & Main Runner
├── models.py        # Database Blueprints (UUID, JSONB, FKs)
├── routes.py        # Core Logic (CRUD, Filter, Validation)
├── reset_db.py      # Database Maintenance & Seeding Tool
├── config.py        # Environment Configuration
├── templates/       # Premium Sidebar Layouts
└── static/          # "Side-Bar" Design Tokens & UI
```

---

## 🧪 Edge Cases Handled
- [x] **Negative Amounts**: Rejected with descriptive flash messages.
- [x] **Invalid Date Logic**: Prevents filters where 'Start' is after 'End'.
- [x] **Referential Integrity**: Categories cannot be deleted if expenses depend on them.
- [x] **Zero-Data State**: Beautifully handled "Empty State" UI.

---

## 💻 Local Setup (Manual)
1. `pip install -r requirements.txt`
2. Update `.env` with your Postgres credentials (default: `root`).
3. Run maintenance: `python reset_db.py`
4. Start app: `python app.py`
