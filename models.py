from extensions import db
from datetime import date
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color_hex = db.Column(db.String(7), nullable=False, default="#888888")
    icon_name = db.Column(db.String(50))
    is_system = db.Column(db.Boolean, nullable=False, default=True)

    expenses = db.relationship("Expense", backref="category", lazy=True)

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), db.CheckConstraint('amount > 0'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class ExpenseAudit(db.Model):
    __tablename__ = "expense_audit"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(UUID(as_uuid=True), db.ForeignKey("expenses.id", ondelete="SET NULL"))
    action = db.Column(db.String(10), nullable=False) # INSERT, UPDATE, DELETE
    old_values = db.Column(JSONB)
    new_values = db.Column(JSONB)
    changed_at = db.Column(db.DateTime, server_default=db.func.now())
