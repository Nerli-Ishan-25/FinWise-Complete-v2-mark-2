import os
import sys
from datetime import datetime

# Add to path so 'app' is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user_finance import User, Asset, Liability, Income, Expense, Category, Budget
from app.core.security import get_password_hash

def seed_users():
    db = SessionLocal()
    
    # User A - Good Financial Health
    usera = db.query(User).filter(User.email == "usera@test.com").first()
    if not usera:
        usera = User(name="User A Good", email="usera@test.com", password_hash=get_password_hash("12345678"), onboarded=True)
        db.add(usera)
        db.commit()
        db.refresh(usera)
        
        # User A Incomes
        db.add(Income(user_id=usera.id, amount=12000, source="Salary", description="Tech Job"))
        db.add(Income(user_id=usera.id, amount=1500, source="Investments", description="Dividends"))
        
        # User A Assets
        db.add(Asset(user_id=usera.id, name="House", type="Real Estate", value=600000))
        db.add(Asset(user_id=usera.id, name="Index Funds", type="Stocks", value=150000))
        db.add(Asset(user_id=usera.id, name="Emergency Fund", type="Cash", value=30000))
        
        # User A Liabilities
        db.add(Liability(user_id=usera.id, name="Mortgage", type="Loan", amount=200000, interest_rate=3.5))
        
        # User A Categories
        catA_housing = Category(user_id=usera.id, name="Housing", type="Expense")
        catA_food = Category(user_id=usera.id, name="Food", type="Expense")
        db.add(catA_housing)
        db.add(catA_food)
        db.commit()
        
        # User A Budgets
        now = datetime.now()
        db.add(Budget(user_id=usera.id, category_id=catA_housing.id, budget_amount=2500, month=now.month, year=now.year))
        db.add(Budget(user_id=usera.id, category_id=catA_food.id, budget_amount=600, month=now.month, year=now.year))
        
        # User A Expenses (within budget)
        db.add(Expense(user_id=usera.id, category="Housing", amount=2000, description="Mortgage payment"))
        db.add(Expense(user_id=usera.id, category="Food", amount=450, description="Groceries"))
        
        db.commit()
        print("User A created successfully.")
    else:
        print("User A already exists.")

    # User B - Bad Financial Health
    userb = db.query(User).filter(User.email == "userb@test.com").first()
    if not userb:
        userb = User(name="User B Bad", email="userb@test.com", password_hash=get_password_hash("12345678"), onboarded=True)
        db.add(userb)
        db.commit()
        db.refresh(userb)
        
        # User B Incomes
        db.add(Income(user_id=userb.id, amount=3500, source="Salary", description="Retail Job"))
        
        # User B Assets
        db.add(Asset(user_id=userb.id, name="Used Car", type="Vehicle", value=4000))
        db.add(Asset(user_id=userb.id, name="Checking Account", type="Cash", value=500))
        
        # User B Liabilities
        db.add(Liability(user_id=userb.id, name="Credit Card Debt", type="Credit Card", amount=18000, interest_rate=24.99))
        db.add(Liability(user_id=userb.id, name="Personal Loan", type="Loan", amount=12000, interest_rate=15.0))
        db.add(Liability(user_id=userb.id, name="Payday Loan", type="Loan", amount=2000, interest_rate=200.0))
        
        # User B Categories
        catB_shopping = Category(user_id=userb.id, name="Shopping", type="Expense")
        catB_food = Category(user_id=userb.id, name="Food", type="Expense")
        db.add(catB_shopping)
        db.add(catB_food)
        db.commit()
        
        # User B Budgets
        now = datetime.now()
        db.add(Budget(user_id=userb.id, category_id=catB_shopping.id, budget_amount=200, month=now.month, year=now.year))
        db.add(Budget(user_id=userb.id, category_id=catB_food.id, budget_amount=400, month=now.month, year=now.year))
        
        # User B Expenses (way over budget)
        db.add(Expense(user_id=userb.id, category="Shopping", amount=1500, description="Designer clothes"))
        db.add(Expense(user_id=userb.id, category="Food", amount=850, description="Eating out every day"))
        
        db.commit()
        print("User B created successfully.")
    else:
        print("User B already exists.")
        
    db.close()

if __name__ == "__main__":
    seed_users()
