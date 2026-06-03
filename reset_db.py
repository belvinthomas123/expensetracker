from app import create_app
from extensions import db
from models import Category, Expense, ExpenseAudit
from sqlalchemy import text
from datetime import date, timedelta

def reset():
    app = create_app()
    with app.app_context():
        print("Dropping old tables...")
        for table in ['expense_audit', 'expenses', 'categories']:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        db.session.commit()
        
        print("Recreating new tables...")
        db.create_all()
        
        print("Seeding categories...")
        food = Category(name='Food', color_hex='#F97316', icon_name='ti-tools-kitchen-2')
        trans = Category(name='Transport', color_hex='#3B82F6', icon_name='ti-car')
        shop = Category(name='Shopping', color_hex='#8B5CF6', icon_name='ti-shopping-bag')
        bills = Category(name='Bills', color_hex='#EF4444', icon_name='ti-receipt')
        ent = Category(name='Entertainment', color_hex='#EC4899', icon_name='ti-confetti')
        other = Category(name='Other', color_hex='#6B7280', icon_name='ti-dots')
        
        categories = [food, trans, shop, bills, ent, other]
        db.session.add_all(categories)
        db.session.commit()

        print("Seeding sample expenses...")
        today = date.today()
        
        samples = [
            Expense(title="Organic Groceries", amount=1250.50, category=food, expense_date=today, note="Weekly stock up"),
            Expense(title="Uber to Office", amount=450.00, category=trans, expense_date=today - timedelta(days=1), note="Monsoon surge pricing"),
            Expense(title="Netflix Subscription", amount=199.00, category=ent, expense_date=today - timedelta(days=2), note="Monthly plan"),
            Expense(title="Internet Bill", amount=999.00, category=bills, expense_date=today - timedelta(days=3), note="Airtel Fiber"),
            Expense(title="Nike Running Shoes", amount=5499.00, category=shop, expense_date=today - timedelta(days=5), note="New Year resolution gear")
        ]
        
        db.session.add_all(samples)
        db.session.commit()
        
        # Add a few audit logs for sample realism
        for s in samples:
            audit = ExpenseAudit(expense_id=s.id, action="INSERT", new_values={"title": s.title, "amount": float(s.amount)})
            db.session.add(audit)
        
        db.session.commit()
        print("Database successfully reset, seeded, and populated with sample data!")

if __name__ == "__main__":
    reset()
