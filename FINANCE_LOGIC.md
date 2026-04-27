# 📊 Financial Logic Behind the App — A Complete Guide

This document explains every financial concept, formula, and decision framework used in this personal finance application. No code — just the **money logic**.

---

## Table of Contents

1. [Net Worth Calculation](#1-net-worth-calculation)
2. [Savings Rate Calculation](#2-savings-rate-calculation)
3. [Budget Planner Logic](#3-budget-planner-logic)
4. [Loan Calculations & EMI](#4-loan-calculations--emi)
5. [AI Loan Eligibility Assessment](#5-ai-loan-eligibility-assessment)
6. [Financial Health Score](#6-financial-health-score)
7. [Financial Insights & Recommendations](#7-financial-insights--recommendations)
8. [Expense Forecasting](#8-expense-forecasting)
9. [Net Worth History Projection](#9-net-worth-history-projection)
10. [Key Financial Ratios Explained](#10-key-financial-ratios-explained)

---

## 1. Net Worth Calculation

**Net Worth** is the single most important snapshot of your financial position. It answers the question: *"If I settled every debt today, how much would I have left?"*

### Formula

```
Net Worth = Total Assets − Total Liabilities
```

### What counts as an Asset?

Assets are things you **own** that hold monetary value:

| Asset Type | Example |
|------------|---------|
| Savings | Bank account, FD, cash |
| Stocks | Equity holdings, mutual funds |
| Crypto | Bitcoin, Ethereum, altcoins |
| Property | Home, land, commercial real estate |
| Other | Gold, vehicle, business ownership |

### What counts as a Liability?

Liabilities are amounts you **owe** to others:

| Liability Type | Example |
|----------------|---------|
| Home Loan | Outstanding mortgage principal |
| Car Loan | Remaining auto loan balance |
| Personal Loan | Consumer debt |
| Credit Card Debt | Revolving balance |
| Education Loan | Student loan outstanding |

### Interpreting the Result

| Net Worth | What It Means |
|-----------|---------------|
| **Positive & Growing** | You own more than you owe — financially healthy |
| **Positive but flat** | Wealth is stagnant — review asset allocation |
| **Zero** | Assets exactly cancel liabilities — break-even |
| **Negative** | Liabilities exceed assets — priority: reduce debt immediately |

> ⚠️ **The app alerts you** when your net worth turns negative and recommends focusing on debt repayment before any new borrowing.

### Net Worth is a Snapshot, Not a Score

Net worth fluctuates daily as asset prices change (e.g., stock or crypto values). What matters more than the absolute number is the **trend over time** — the app tracks this month-by-month.

---

## 2. Savings Rate Calculation

The **Savings Rate** tells you what percentage of your income you are actually keeping. It is widely regarded as the most powerful indicator of long-term financial health.

### Formula

```
Savings Rate (%) = ((Monthly Income − Monthly Expenses) / Monthly Income) × 100
```

### Example

- Monthly Income: ₹80,000
- Monthly Expenses: ₹60,000
- Savings: ₹20,000
- Savings Rate = (20,000 / 80,000) × 100 = **25%**

### Interpreting Savings Rate

| Savings Rate | Interpretation |
|--------------|----------------|
| **< 0%** | You are spending more than you earn — deficit spending |
| **0% – 5%** | Very low buffer; one emergency could destabilize you |
| **5% – 15%** | Moderate — building savings slowly |
| **15% – 30%** | Healthy — on track for meaningful wealth accumulation |
| **> 30%** | Excellent — aggressive savings, financial independence path |

### Why This Matters More Than the Absolute Savings Amount

Someone saving ₹5,000 out of ₹15,000 income (33%) is in a better financial position than someone saving ₹20,000 out of ₹1,00,000 income (20%), despite the larger absolute amount. The **ratio relative to income** is what the app optimizes for.

> 💡 **The app calculates savings rate on the current calendar month only** — income and expenses entered before the 1st of the current month are excluded from this figure. This gives you a real-time, month-in-progress view.

---

## 3. Budget Planner Logic

The app implements a **Zero-Based Budgeting (ZBB)** framework — every rupee of income is assigned a purpose.

### Core Concept: Zero-Based Budgeting

In ZBB, you start each month with your income and allocate it completely:

```
Income − All Budget Allocations = 0 (ideally)
```

Any money not assigned to a category is called **Unallocated**. The app highlights this and nudges you to give every rupee a job.

### How Budgets are Structured

Each budget entry has:
- **Category** — e.g., Housing, Food, Transport, Health
- **Budget Amount** — the cap you set for that category this month
- **Spent** — actual expenses logged under that category
- **Remaining** — Budget Amount minus Spent

### Budget Utilization

For each category:

```
Utilization % = (Spent / Budget) × 100
```

The app uses a traffic-light colour system:
- 🟢 **Green** (< 80%) — on track
- 🟡 **Amber** (80–99%) — approaching limit
- 🔴 **Red** (≥ 100%) — over budget

### Frequency Normalization

When you enter a budget, you can specify it weekly, monthly, or yearly. The app normalizes everything to **monthly equivalents**:

| Your Input | Conversion |
|------------|-----------|
| Weekly amount | × (52 ÷ 12) ≈ × 4.333 |
| Monthly amount | No change |
| Yearly amount | ÷ 12 |

This is because a month has approximately 4.333 weeks (52 weeks ÷ 12 months), not exactly 4.

### Unallocated Funds

```
Unallocated = Monthly Income − Total Budgeted
```

If Unallocated > 0, the app alerts you that you have money without a plan. In ZBB, this remainder should be assigned to savings, investments, or an emergency fund category.

### Uncategorized Spending

The app also detects **expenses that don't match any budget category**. This is spending that happened but wasn't planned — it represents budget leakage and is surfaced as an additional warning.

---

## 4. Loan Calculations & EMI

### What is EMI?

**Equated Monthly Instalment (EMI)** is the fixed monthly payment you make to repay a loan. Each payment covers both interest for the month and a portion of the principal (the original borrowed amount).

### Standard EMI Formula (Amortisation)

```
EMI = P × r × (1 + r)^n / ((1 + r)^n − 1)
```

Where:
- **P** = Principal (loan amount)
- **r** = Monthly interest rate = Annual interest rate ÷ 12
- **n** = Loan term in months

### Example

- Loan: ₹5,00,000
- Annual interest rate: 12% → Monthly rate r = 1% = 0.01
- Tenure: 36 months

```
EMI = 5,00,000 × 0.01 × (1.01)^36 / ((1.01)^36 − 1)
    = 5,00,000 × 0.01 × 1.4308 / 0.4308
    = ₹16,607 per month
```

### How Interest and Principal Split Changes Over Time

In every EMI, the proportion of interest vs. principal changes:

- **Early months**: Most of the EMI is interest (because outstanding principal is high)
- **Later months**: Gradually more goes to principal (interest reduces as balance shrinks)

This is why prepaying a loan **early** saves significantly more interest than prepaying later.

### The App's EMI Estimation (in Loan Assessment)

For the loan eligibility model, the app uses the **DTI Ratio as a proxy for monthly rate** to estimate EMI:

```
Monthly rate (r) = DTI Ratio ÷ 12
EMI = Loan × (r × (1+r)^term) / ((1+r)^term − 1)

If rate ≈ 0:
EMI = Loan ÷ Term   (simple division — flat equal payments)
```

This is an approximation used for risk scoring, not a precise repayment schedule.

---

## 5. AI Loan Eligibility Assessment

The app uses a trained **XGBoost machine learning model** to predict whether a loan application is likely to be approved or rejected by a lender. This mimics how banks actually score loan applications.

### What is XGBoost?

XGBoost (Extreme Gradient Boosting) is a decision-tree-based algorithm that learns patterns from thousands of past loan outcomes (approved vs. defaulted) to predict risk on new applications.

### The Decision Threshold

```
If P(default) ≥ 0.6387  →  REJECTED (High Default Risk)
If P(default) <  0.6387  →  APPROVED (Within Acceptable Risk)
```

The threshold of **63.87%** was optimized during model training to balance two types of errors:
- False positives (approving bad loans = financial loss for lender)
- False negatives (rejecting good loans = lost business)

### Input Features the Model Considers

**Borrower Profile:**

| Feature | What It Captures |
|---------|-----------------|
| Age | Life stage and income stability expectation |
| Annual Income | Repayment capacity |
| Credit Score (300–850) | History of honouring past debts |
| Months Employed | Job stability |
| Number of Credit Lines | Credit usage breadth |
| Education Level | Proxy for earning potential |
| Employment Type | Income reliability (Full-time > Self-employed > Unemployed) |
| Marital Status | Household financial resilience |
| Has Mortgage | Existing major obligation |
| Has Dependents | Impact on disposable income |
| Has Co-Signer | Risk sharing with a guarantor |

**Loan Details:**

| Feature | What It Captures |
|---------|-----------------|
| Loan Amount | Size of obligation |
| Loan Term (months) | Repayment duration |
| DTI Ratio | Current debt burden relative to income |
| Loan Purpose | Risk profile of use (Home < Auto < Business < Other) |

### Engineered Features (Derived Ratios)

Beyond raw inputs, the model was trained on three computed ratios that have high predictive power:

**1. Loan-to-Income Ratio**
```
Loan_to_Income = Loan Amount ÷ Annual Income
```
Measures how large the loan is relative to what you earn. A ratio > 5x is considered high risk.

**2. EMI-to-Income Ratio**
```
EMI_to_Income = Monthly EMI ÷ Monthly Income
```
Measures whether your monthly repayment is affordable within your income. Lenders typically prefer this below 40–50%.

**3. Credit per Line**
```
Credit_per_Line = Loan Amount ÷ Number of Credit Lines
```
Measures average credit exposure per credit line. High values may signal concentration risk.

### Risk Levels

| Default Probability | Risk Level |
|--------------------|-----------|
| < 35% | 🟢 Low |
| 35% – 63.87% | 🟡 Moderate |
| ≥ 63.87% | 🔴 High (Rejected) |

### Confidence Score

```
Confidence % = |P(default) − 0.5| × 200
```

This measures how far the prediction is from the uncertain midpoint (50%). A prediction of 90% default probability gives 80% confidence; a prediction of 55% gives only 10% confidence.

### Key Factors Explained

The model surfaces up to 5 human-readable factors explaining the verdict:

| Factor | Threshold | Interpretation |
|--------|-----------|----------------|
| Credit Score ≥ 720 | Excellent | Strong repayment history |
| Credit Score ≤ 580 | Poor | Significant default risk signal |
| DTI < 28% | Healthy | Low existing debt burden |
| DTI > 43% | High | Debt is consuming too much income |
| Loan-to-Income > 5x | High | Loan is very large relative to earnings |
| Employment < 12 months | Short | Job instability increases risk |
| Employment ≥ 36 months | Stable | Consistent income source |
| Co-signer = Yes | Mitigant | Reduces lender's risk |
| Mortgage = Yes | Burden | Additional major obligation |

---

## 6. Financial Health Score

The app generates a **score from 0 to 10** representing overall financial health. It is a heuristic (rule-based) model, not machine learning.

### Scoring Components

**Base score: 5.0 (neutral starting point)**

The base is then adjusted up or down based on three factors:

#### Component 1: Savings Rate (up to +3 / −2 points)

| Savings Rate | Adjustment |
|-------------|-----------|
| ≥ 20% | +3 |
| 10% – 19% | +2 |
| 5% – 9% | +1 |
| 0% – 4% | No change |
| Negative | −2 |

#### Component 2: Emergency Fund Ratio (up to +2 points)

The emergency fund ratio is how many months of expenses your savings can cover.

| Emergency Fund Coverage | Adjustment |
|------------------------|-----------|
| ≥ 6 months of expenses | +2 |
| 3–5 months | +1 |
| < 3 months | No change |

> 📌 The app uses a **default assumed ratio of 3.0** for this component when not specifically tracked.

#### Component 3: Debt-to-Income Ratio (up to −3 points)

The debt-to-income ratio is total monthly debt payments as a fraction of monthly income.

| DTI Ratio | Adjustment |
|-----------|-----------|
| < 30% | No penalty |
| 30% – 39% | −1 |
| 40% – 59% | −2 |
| ≥ 60% | −3 |

### Score Interpretation

| Score | Financial Health |
|-------|-----------------|
| 8–10 | Excellent |
| 6–7 | Good |
| 4–5 | Fair — room for improvement |
| 0–3 | Poor — immediate action needed |

---

## 7. Financial Insights & Recommendations

The app generates automated text insights based on your current metrics. Each recommendation is triggered by a specific rule.

### Savings Rate Recommendations

| Condition | Recommendation Generated |
|-----------|--------------------------|
| Savings Rate < 0% | You are spending more than you earn. Cut discretionary expenses to reach break-even. |
| 0% – 5% | Low savings rate. Aim for 5–10% as a safety buffer. |
| 5% – 15% | Healthy savings. Consider automating transfers into savings or investments. |
| ≥ 15% | Excellent rate. Review your investment plan to put extra cash to work. |

### Net Worth Recommendations

| Condition | Recommendation Generated |
|-----------|--------------------------|
| Net Worth < 0 | Negative net worth. Focus on high-interest debt. Avoid new borrowing. |
| Net Worth < 3× Monthly Income | Build an emergency fund worth 3–6 months of expenses. |

### Expense-to-Income Recommendations

| Expense Ratio (Expenses ÷ Income) | Recommendation Generated |
|-----------------------------------|--------------------------|
| > 80% | Expenses are consuming most of income. Review subscriptions and large categories. |
| < 50% | Comfortable gap. Consider directing more toward long-term goals. |

### The 50/30/20 Context

While the app doesn't enforce a specific budgeting rule, the thresholds used (50%, 80%) are grounded in widely accepted frameworks:
- **50%** for needs (housing, food, transport)
- **30%** for wants (entertainment, dining out)
- **20%** for savings and debt repayment

---

## 8. Expense Forecasting

The app predicts your **next month's expenses** using a straightforward averaging model.

### Method: Rolling Average

```
Forecasted Next Month = Average of all past expense amounts
```

This is a **mean-based forecast** — it smooths out anomalous months and gives a stable expected baseline.

### Why Simple Averaging?

More sophisticated models (linear regression, ARIMA) require larger datasets to be accurate. For a personal finance app with potentially only weeks of history, the mean of observed expenses is both:
- **Robust** — not distorted by one unusual month
- **Honest** — doesn't pretend to have more signal than the data contains

### How to Read the Forecast

The forecasted figure represents your expected spending if you behave similarly to your past patterns. If your actual budget is lower than the forecast, you need to consciously change behaviour.

---

## 9. Net Worth History Projection

The app shows a **month-by-month net worth history chart**, even though it only stores current asset and liability values. It reconstructs the past using this logic:

### Backward Reconstruction Formula

```
Starting point: Current Net Worth = Current Assets − Current Liabilities

For each past month (working backwards):
  Net Worth [month-N] = Net Worth [month-N+1] − (Income[N] − Expenses[N])
```

In plain English: *"If you earned ₹80K and spent ₹60K last month, your net worth must have been ₹20K lower the month before."*

### Limitations

This is a **retrospective estimate**, not a recorded history. It assumes:
- Asset and liability values have not changed (no property appreciation, no loan repayments changing the liability balance)
- All income and expenses are captured in transactions

It is useful for spotting **trend direction** but should not be treated as a precise historical record.

---

## 10. Key Financial Ratios Explained

### Debt-to-Income (DTI) Ratio

```
DTI = Total Monthly Debt Payments ÷ Gross Monthly Income
```

Used by lenders to assess repayment capacity.

| DTI | Lender Interpretation |
|-----|----------------------|
| < 28% | Excellent — low debt burden |
| 28–36% | Good — manageable |
| 36–43% | Borderline — approaching risky |
| > 43% | High risk — most lenders decline |

### Loan-to-Income Ratio

```
LTI = Total Loan Amount ÷ Annual Income
```

Measures affordability of total debt load. Most lenders cap this at 3–5x annual income for personal loans.

### Savings Rate

```
Savings Rate = (Income − Expenses) ÷ Income × 100
```

The most actionable personal finance metric — the percentage of income you keep.

### Emergency Fund Ratio

```
Emergency Fund Ratio = Liquid Savings ÷ Monthly Expenses
```

Measures how many months you could survive on savings alone if income stopped. Financial planners recommend 3–6 months.

### Budget Utilization Rate

```
Utilization = Actual Spending ÷ Budgeted Amount × 100
```

Per-category metric. Above 100% means you overspent your planned limit.

### Net Worth-to-Income Ratio

```
NW/Income = Net Worth ÷ Annual Income
```

A rough wealth benchmark. A common rule of thumb (the "Millionaire Next Door" formula):

```
Expected Net Worth = Age × Annual Income ÷ 10
```

This is a benchmark, not a target — it varies significantly by life stage.

---

## Summary: The Financial Logic Chain

```
Income & Expenses
       ↓
  Savings Rate  ────────────────────────┐
       ↓                                │
  Budget Planner (ZBB)                  │
       ↓                                ↓
  Assets & Liabilities          Financial Health Score (0–10)
       ↓                                │
   Net Worth                            │
       ↓                         Insights & Recommendations
  Net Worth History
  
  (Parallel Track)
  Loan Application → AI XGBoost Model → Eligibility Verdict
                   → DTI, LTI, EMI-to-Income ratios
                   → Risk Level + Key Factors
```

Every number in the app flows from two root inputs: **what you earn** and **what you spend**. Everything else — net worth, health score, budget utilization, loan risk — is derived from those two fundamental truths.

---

*This document reflects the financial logic as implemented in the app. All formulas are standard personal finance conventions used by financial planners and lending institutions worldwide.*
