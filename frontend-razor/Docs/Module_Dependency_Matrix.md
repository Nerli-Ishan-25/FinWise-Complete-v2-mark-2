# Module Dependency Matrix

This matrix maps the high-level FinWise modules to their underlying dependencies to ensure a complete and correct migration to Razor Pages.

| Logical Module | Frontend Pages (Razor) | APIs Used (FastAPI) | Database Entities | Shared Razor Components |
|---|---|---|---|---|
| **Authentication** | `Login.cshtml`, `Register.cshtml`, `Onboarding.cshtml` | `/api/v1/auth/*`, `/api/v1/finance/profile` | `User` | `AuthLayout.cshtml` |
| **Dashboard** | `Index.cshtml` (Dashboard) | `/api/v1/finance/dashboard`, `/api/v1/finance/transactions`, `/api/v1/insights/` | `Transaction`, `Income`, `Expense` | `SummaryCard.cshtml`, `RecentTransactions.cshtml`, `ChartCanvas.cshtml` |
| **Expense Tracker** | `Expenses/Index.cshtml`, `Expenses/Add.cshtml`, `Expenses/Edit.cshtml` | `/api/v1/finance/expenses`, `/api/v1/finance/transactions`, `/api/v1/categories/` | `Expense`, `Category`, `Transaction` | `DataTable.cshtml`, `ExpenseForm.cshtml` |
| **Income Tracker** | `Income/Index.cshtml`, `Income/Add.cshtml`, `Income/Edit.cshtml` | `/api/v1/finance/income`, `/api/v1/finance/transactions`, `/api/v1/categories/` | `Income`, `Category`, `Transaction` | `DataTable.cshtml`, `IncomeForm.cshtml` |
| **Budget Planner** | `Budgets/Index.cshtml`, `Budgets/Manage.cshtml` | `/api/v1/budgets/*`, `/api/v1/categories/` | `Budget`, `Category` | `BudgetProgress.cshtml`, `BudgetForm.cshtml` |
| **Net Worth Tracker** | `NetWorth/Index.cshtml` | `/api/v1/finance/net-worth`, `/api/v1/assets/*`, `/api/v1/liabilities/*` | `Asset`, `Liability` | `AssetList.cshtml`, `LiabilityList.cshtml`, `NetWorthChart.cshtml` |
| **Loan Analyzer** | `LoanAnalyzer/Index.cshtml`, `LoanAnalyzer/Results.cshtml` | `/api/v1/loan-assessment/*` | `LoanAssessment` | `LoanInputForm.cshtml`, `PredictionGauge.cshtml` |
| **AI Assistant** | `Assistant/Index.cshtml` | `/api/v1/assistant/chat` | `ChatHistory` (if persisted) | `ChatWindow.cshtml`, `MessageBubble.cshtml` |
| **Subscriptions** | `Subscriptions/Index.cshtml` | `/api/v1/subscriptions/*` | `Subscription` | `DataTable.cshtml`, `SubscriptionForm.cshtml` |

## Migration Notes
- **Razor Pages NEVER accesses SQLite directly.** The "Database Entities" column is merely for understanding what domain models the APIs manipulate. All data operations flow through HttpClient calls to FastAPI.
- **Shared Components** will be implemented as Razor Partial Views (`_PartialName.cshtml`) or View Components in the Razor Pages structure.
