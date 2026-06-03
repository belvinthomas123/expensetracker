from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Expense, Category, ExpenseAudit
from datetime import date, datetime
from sqlalchemy import func

main = Blueprint("main", __name__)

@main.route("/")
def index():
    category_id = request.args.get("category_id", "")
    title = request.args.get("title", "")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    query = Expense.query.join(Category)

    if title:
        query = query.filter(Expense.title.ilike(f"%{title}%"))
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    if from_date and to_date:
        if from_date > to_date:
            flash("Filter Warning: 'From Date' cannot be after 'To Date'.")
            return redirect(url_for("main.index"))

    if from_date:
        try:
            query = query.filter(Expense.expense_date >= datetime.strptime(from_date, "%Y-%m-%d").date())
        except ValueError:
            pass
    if to_date:
        try:
            query = query.filter(Expense.expense_date <= datetime.strptime(to_date, "%Y-%m-%d").date())
        except ValueError:
            pass

    expenses = query.order_by(Expense.expense_date.desc()).all()

    # Categories for the dropdown
    categories = Category.query.all()

    # Premium Summary with Real SQL JOIN & Aggregation
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    
    total = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.expense_date >= start_of_month
    ).scalar()

    breakdown = db.session.query(
        Category.name,
        func.sum(Expense.amount).label('total'),
        Category.color_hex
    ).join(Expense).filter(
        Expense.expense_date >= start_of_month
    ).group_by(Category.id, Category.name, Category.color_hex).order_by(func.sum(Expense.amount).desc()).all()

    return render_template("index.html", 
                         expenses=expenses, 
                         total=total, 
                         breakdown=breakdown,
                         categories=categories,
                         today=today.strftime('%Y-%m-%d'),
                         now=today)

@main.route("/add", methods=["POST"])
def add():
    try:
        title = request.form.get("title", "").strip()
        amount_str = request.form.get("amount", "0")
        category_id = request.form.get("category_id")
        expense_date_str = request.form.get("expense_date")
        note = request.form.get("note", "").strip()

        # Validation
        if not title:
            flash("Error: Title is required.")
            return redirect(url_for("main.index"))

        try:
            amount = float(amount_str)
            if amount <= 0:
                flash("Error: Amount must be a positive number.")
                return redirect(url_for("main.index"))
        except ValueError:
            flash("Error: Invalid amount format.")
            return redirect(url_for("main.index"))

        expense = Expense(
            title=title,
            amount=amount,
            category_id=category_id,
            expense_date=datetime.strptime(expense_date_str, "%Y-%m-%d").date(),
            note=note
        )
        db.session.add(expense)
        db.session.commit()

        # Audit Log (JSONB)
        audit = ExpenseAudit(
            expense_id=expense.id,
            action="INSERT",
            new_values={"title": title, "amount": amount, "date": expense_date_str}
        )
        db.session.add(audit)
        db.session.commit()

        flash("Expense recorded successfully!")
    except Exception as e:
        flash(f"System Error: {str(e)}")
    
    return redirect(url_for("main.index"))

@main.route("/delete/<string:id>")
def delete(id):
    expense = Expense.query.get_or_404(id)
    
    # Audit before delete
    audit = ExpenseAudit(
        expense_id=expense.id,
        action="DELETE",
        old_values={"title": expense.title, "amount": float(expense.amount)}
    )
    db.session.add(audit)
    
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.")
    return redirect(url_for("main.index"))

@main.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id):
    expense = Expense.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == "POST":
        try:
            old_data = {"title": expense.title, "amount": float(expense.amount)}
            
            expense.title = request.form["title"]
            expense.amount = float(request.form["amount"])
            expense.category_id = request.form["category_id"]
            expense.expense_date = datetime.strptime(request.form["expense_date"], "%Y-%m-%d").date()
            expense.note = request.form["note"]
            
            new_data = {"title": expense.title, "amount": float(expense.amount)}
            
            # Audit Update
            audit = ExpenseAudit(
                expense_id=expense.id,
                action="UPDATE",
                old_values=old_data,
                new_values=new_data
            )
            db.session.add(audit)
            
            db.session.commit()
            flash("Expense updated!")
            return redirect(url_for("main.index"))
        except Exception as e:
            flash(f"Error updating expense: {str(e)}")

    return render_template("edit.html", expense=expense, categories=categories, now=date.today())
