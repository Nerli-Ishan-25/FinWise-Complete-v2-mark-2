# API Inventory

This document outlines every FastAPI endpoint currently used in the FinWise application.

## Authentication (`/api/v1/auth`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/auth/register` | `UserCreate` | `UserInDB` | No | Register a new user |
| POST | `/api/v1/auth/login` | `OAuth2PasswordRequestForm` | `Token` | No | Login and get JWT |
| POST | `/api/v1/auth/onboarding` | `OnboardingData` | `UserInDB` | Yes | Complete user onboarding |

## Finance (`/api/v1/finance`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| GET | `/api/v1/finance/dashboard` | None | `DashboardMetrics` | Yes | Get overall dashboard stats |
| GET | `/api/v1/finance/monthly-summary` | None | `List[MonthlySummaryItem]` | Yes | Get monthly income/expense summary |
| GET | `/api/v1/finance/income` | None | `List[IncomeResponse]` | Yes | Get user income records |
| POST | `/api/v1/finance/income` | `IncomeCreate` | `IncomeResponse` | Yes | Add new income record |
| PUT | `/api/v1/finance/update-income` | `IncomeUpdateRequest` | `IncomeResponse` | Yes | Update total monthly income |
| GET | `/api/v1/finance/expenses` | None | `List[ExpenseResponse]` | Yes | Get user expense records |
| POST | `/api/v1/finance/expenses` | `ExpenseCreate` | `ExpenseResponse` | Yes | Add new expense record |
| GET | `/api/v1/finance/loans` | None | `List[LoanResponse]` | Yes | Get active loans |
| POST | `/api/v1/finance/loans` | `LoanCreate` | `LoanResponse` | Yes | Add a new loan |
| DELETE | `/api/v1/finance/loans/{loan_id}` | None | None | Yes | Delete a loan |
| GET | `/api/v1/finance/transactions` | None | `List[TransactionResponse]` | Yes | Get recent transactions |
| DELETE | `/api/v1/finance/transactions/{id}` | None | None | Yes | Delete a transaction |
| GET | `/api/v1/finance/net-worth` | None | `float` (value) | Yes | Get calculated net worth |
| GET | `/api/v1/finance/profile` | None | `UserInDB` | Yes | Get user profile info |
| PUT | `/api/v1/finance/profile` | `UserUpdate` | `UserInDB` | Yes | Update user profile info |

## Categories (`/api/v1/categories`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/categories/` | `CategoryCreate` | `CategoryResponse` | Yes | Create category |
| GET | `/api/v1/categories/` | None | `List[CategoryResponse]` | Yes | List categories |
| DELETE | `/api/v1/categories/{id}` | None | None | Yes | Delete category |

## Budgets (`/api/v1/budgets`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/budgets/` | `BudgetCreate` | `BudgetResponse` | Yes | Create budget |
| GET | `/api/v1/budgets/` | None | `List[BudgetResponse]` | Yes | List budgets |
| PUT | `/api/v1/budgets/{id}` | `BudgetUpdate` | `BudgetResponse` | Yes | Update budget |
| DELETE | `/api/v1/budgets/{id}` | None | None | Yes | Delete budget |

## Assets (`/api/v1/assets`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/assets/` | `AssetCreate` | `AssetResponse` | Yes | Create asset |
| GET | `/api/v1/assets/` | None | `List[AssetResponse]` | Yes | List assets |
| PUT | `/api/v1/assets/{id}` | `AssetUpdate` | `AssetResponse` | Yes | Update asset |
| DELETE | `/api/v1/assets/{id}` | None | None | Yes | Delete asset |

## Liabilities (`/api/v1/liabilities`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/liabilities/` | `LiabilityCreate` | `LiabilityResponse` | Yes | Create liability |
| GET | `/api/v1/liabilities/` | None | `List[LiabilityResponse]` | Yes | List liabilities |
| PUT | `/api/v1/liabilities/{id}` | `LiabilityUpdate` | `LiabilityResponse` | Yes | Update liability |
| DELETE | `/api/v1/liabilities/{id}` | None | None | Yes | Delete liability |

## Subscriptions (`/api/v1/subscriptions`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/subscriptions/` | `SubscriptionCreate` | `SubscriptionResponse` | Yes | Create subscription |
| GET | `/api/v1/subscriptions/` | None | `List[SubscriptionResponse]` | Yes | List subscriptions |
| PUT | `/api/v1/subscriptions/{id}` | `SubscriptionUpdate` | `SubscriptionResponse` | Yes | Update subscription |
| DELETE | `/api/v1/subscriptions/{id}` | None | None | Yes | Delete subscription |

## AI Assistant & Machine Learning
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/loan-assessment/predict` | `LoanData` (features) | `LoanAssessmentResponse` | Yes | Predict loan approval via XGBoost |
| GET | `/api/v1/loan-assessment/` | None | `List[LoanAssessmentResponse]` | Yes | Get historical predictions |
| POST | `/api/v1/assistant/chat` | `ChatRequest` (message) | `ChatResponse` (reply) | Yes | Chat with AI (Ollama/Gemini) |
| GET | `/api/v1/insights/` | None | `List[str]` | Yes | Fetch dynamically generated AI insights |

## Admin (`/api/v1/admin`)
| Method | Endpoint | Request Payload | Response Payload | Auth Required | Description |
|---|---|---|---|---|---|
| POST | `/api/v1/admin/users` | `UserCreate` | `UserInDB` | Yes (Admin) | Create user (Admin) |
| GET | `/api/v1/admin/users` | None | `List[UserInDB]` | Yes (Admin) | List users |
| DELETE | `/api/v1/admin/users/{id}` | None | None | Yes (Admin) | Delete user |
| GET | `/api/v1/admin/analytics` | None | Admin Dashboard Data | Yes (Admin) | Get platform analytics |
