import os
import sys
from datetime import datetime

# Add to path so 'app' is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user_finance import User, Asset, Liability, Expense, Category, Budget

def add_more_data():
    db = SessionLocal()
    now = datetime.now()
    
    # ------------------
    # User A - Good Data
    # ------------------
    usera = db.query(User).filter(User.email == "usera@test.com").first()
    if usera:
        # More Diverse Assets
        db.add_all([
            Asset(user_id=usera.id, name="Bitcoin Holdings", type="Crypto", value=45000),
            Asset(user_id=usera.id, name="Government Bonds", type="Bonds", value=75000),
            Asset(user_id=usera.id, name="Rental Property", type="Real Estate", value=350000),
            Asset(user_id=usera.id, name="401k Retirement", type="Retirement", value=220000),
            Asset(user_id=usera.id, name="Gold ETF", type="Commodity", value=15000)
        ])
        
        # More Diverse Liabilities
        db.add_all([
            Liability(user_id=usera.id, name="Investment Property Mortgage", type="Mortgage", amount=180000, interest_rate=4.1),
            Liability(user_id=usera.id, name="Auto Loan (Tesla)", type="Auto Loan", amount=35000, interest_rate=2.9),
            Liability(user_id=usera.id, name="Student Loan", type="Student Loan", amount=15000, interest_rate=4.5)
        ])
        
        # Categories / Budgets for new Expenses
        categories_to_add = [
            ("Travel", 800), ("Healthcare", 300), ("Insurance", 400), 
            ("Entertainment", 300), ("Utilities", 250), ("Investing", 2000)
        ]
        
        for cat_name, budget_amt in categories_to_add:
            cat = db.query(Category).filter(Category.name == cat_name, Category.user_id == usera.id).first()
            if not cat:
                cat = Category(user_id=usera.id, name=cat_name, type="Expense")
                db.add(cat)
                db.commit() # Commit to get ID
                db.add(Budget(user_id=usera.id, category_id=cat.id, budget_amount=budget_amt, month=now.month, year=now.year))
        
        # 6 New Diverse Expenses (within budget)
        db.add_all([
            Expense(user_id=usera.id, category="Travel", amount=650, description="Flight to Aspen"),
            Expense(user_id=usera.id, category="Healthcare", amount=120, description="Dental checkup"),
            Expense(user_id=usera.id, category="Insurance", amount=350, description="Auto & Home bundle"),
            Expense(user_id=usera.id, category="Entertainment", amount=150, description="Concert tickets"),
            Expense(user_id=usera.id, category="Utilities", amount=180, description="Electricity & Water"),
            Expense(user_id=usera.id, category="Investing", amount=2000, description="Monthly S&P500 contribution")
        ])
        
        db.commit()
        print("Added more data to User A.")
    else:
        print("User A not found.")

    # ------------------
    # User B - Bad Data
    # ------------------
    userb = db.query(User).filter(User.email == "userb@test.com").first()
    if userb:
        # More Diverse Assets (Low value/depreciating)
        db.add_all([
            Asset(user_id=userb.id, name="Pawned Jewelry", type="Collectibles", value=800),
            Asset(user_id=userb.id, name="Old Electronics", type="Electronics", value=300),
            Asset(user_id=userb.id, name="Meme Coins", type="Crypto", value=50),
            Asset(user_id=userb.id, name="Savings Account", type="Cash", value=15) # Very low cash
        ])
        
        # More Diverse Liabilities (High interest/bad debt)
        db.add_all([
            Liability(user_id=userb.id, name="Medical Debt", type="Medical", amount=8500, interest_rate=8.0),
            Liability(user_id=userb.id, name="Owed to Family", type="Personal Loan", amount=5000, interest_rate=0.0),
            Liability(user_id=userb.id, name="IRS Back Taxes", type="Tax Dept", amount=4000, interest_rate=12.0),
            Liability(user_id=userb.id, name="Title Loan", type="Title Loan", amount=1500, interest_rate=300.0)
        ])
        
        # Categories / Budgets for new Expenses
        categories_to_add_b = [
            ("Entertainment", 100), ("Subscriptions", 50), ("Fast Food", 150), 
            ("Fees", 0), ("Transportation", 150), ("Vices", 50)
        ]
        
        for cat_name, budget_amt in categories_to_add_b:
            cat = db.query(Category).filter(Category.name == cat_name, Category.user_id == userb.id).first()
            if not cat:
                cat = Category(user_id=userb.id, name=cat_name, type="Expense")
                db.add(cat)
                db.commit() # Commit to get ID
                db.add(Budget(user_id=userb.id, category_id=cat.id, budget_amount=budget_amt, month=now.month, year=now.year))
        
        # 6 New Diverse Expenses (Over budget / bad habits)
        db.add_all([
            Expense(user_id=userb.id, category="Entertainment", amount=450, description="Night club drinks"),
            Expense(user_id=userb.id, category="Subscriptions", amount=120, description="Multiple unused streaming services"),
            Expense(user_id=userb.id, category="Fast Food", amount=400, description="UberEats and drive-thru"),
            Expense(user_id=userb.id, category="Fees", amount=105, description="Overdraft and late payment fees"),
            Expense(user_id=userb.id, category="Transportation", amount=350, description="Lots of Uber rides"),
            Expense(user_id=userb.id, category="Vices", amount=280, description="Lottery tickets and vaping")
        ])
        
        db.commit()
        print("Added more data to User B.")
    else:
        print("User B not found.")
        
    db.close()

if __name__ == "__main__":
    add_more_data()
