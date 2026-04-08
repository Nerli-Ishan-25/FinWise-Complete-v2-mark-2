# 📘 FinWise AI Finance - User Manual

Welcome to **FinWise**, your AI-powered wealth management and budgeting companion. This guide will walk you through the entire experience, from initial setup to day-to-day financial tracking.

---

## 🚀 1. Getting Started
Before you can manage your finances, you need to launch the application.

### The Easy Way (Automated Script)
1. Open a PowerShell window in the project root.
2. Run `.\start_finwise.ps1`.
3. This will automatically clean up old processes, start the backend/frontend, and open your browser to the login page.

### The Manual Way
If you prefer running components separately:
*   **Backend**: `cd Backend; .\venv\Scripts\python.exe -m app.main`
*   **Frontend**: `cd finwise-frontend; npx vite`
*   Access the app at: `http://localhost:5173`

---

## 🔑 2. Account Access
### Sign Up
1. On the landing page, click **Get Started** or **Sign Up**.
2. Enter your Name, Email, and a secure Password.
3. Once registered, you will be redirected to the **Onboarding** flow.

### Login
1. Use your registered email and password to sign in.
2. If you are already logged in from a previous session, you will bypass the login screen.

---

## 📋 3. Onboarding (First-Time Only)
When you first sign up, FinWise needs to understand your current financial standing:
1. **Financial Profile**: Select your primary financial goal (e.g., "Build Wealth", "Pay Down Debt").
2. **Current Assets**: Enter your current savings, property, or investments.
3. **Current Liabilities**: Enter any debts, loans, or credit card balances.
   - *Note: Enter the full principal amount and the APR (Interest Rate).*
4. **Monthly Income**: Provide your regular income sources.

---

## 📈 4. Financial Management

### Dashboard
The Dashboard is your command center. It shows:
*   **Net Worth**: Your total assets minus total liabilities. If this is negative, it will appear in red.
*   **Monthly Budget**: A summary of your total budget versus your actual spending for the current month.
*   **Recent Transactions**: Your latest income and expense items.
*   **🔄 Sync Button**: If you've just made changes and want to ensure everything is perfectly calculated, hit the **Sync** button in the top right.

### Net Worth Page
Analyze your wealth in detail:
*   **Asset Allocation**: A breakdown of where your money is (Cash, Stocks, Real Estate, etc.).
*   **Liability Breakdown**: A list of all debts. 
   - **Monthly Interest**: Each debt shows an "Interest" value, which is the estimated cost of that debt for the current month based on your APR.
*   **Risk Warning**: If your liabilities exceed your assets, a red warning banner will appear to help you focus on debt reduction.

---

## 💰 5. Budgeting & Expenses

### Budget Planner
Set your limits and track your progress:
1. **Add Category**: Click "Add Category" to set a limit for a specific spending area (e.g., Food, Rent, Entertainment).
2. **Frequency Normalization**: You can set budgets as **Weekly, Monthly, or Yearly**. 
   - *Example: A $50 Weekly coffee budget will be automatically normalized to ~$216.67/month.*
3. **Utilization Bar**: The bar at the top shows your total budgeted amount versus your total spent.
4. **⚠️ Uncategorized**: Any expense you add that doesn't match a budget category will appear in the "Uncategorized" bucket so you can see where "hidden" money is going.

### Expenses
1. Click **Add Transaction** to record a new expense.
2. Ensure you pick a **Category** that matches one of your Budget categories to enable real-time tracking.
3. Once saved, a success notification will appear. You can continue navigating while this notification is visible.

---

## 🔒 6. Ending Your Session
To keep your financial data secure:
1. Click **Log Out** in the sidebar footer.
2. This clears your session tokens and ensures nobody else can access your data from the current browser.
3. **Closing Services**: If you ran the app via terminal, you can close those windows or press `Ctrl+C` to stop the backend/frontend.

---

**Happy Wealth Building!**
*For technical issues, please refer to the README.md in the root directory.*
