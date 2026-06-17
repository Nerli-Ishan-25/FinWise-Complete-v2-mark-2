# FinWise Loan Assessment Use Cases

## Purpose

These use cases are designed to:
* validate the backend loan assessment pipeline,
* demonstrate model behavior across different financial profiles,
* test feature engineering and business-rule thresholds,
* and showcase explainable AI decision outcomes.

---

# User Categories

### User A — Low Risk / Approved
A financially stable user with strong repayment capability and healthy financial metrics.

### User B — Medium Risk / Conditional Approval
A moderate-risk user with acceptable but imperfect financial indicators.

### User C — High Risk / Rejected
A financially stressed user with high debt burden and elevated default probability.

---

# User A: Low Risk / Approved

## 1. Financial Scenario Description
User A is a senior software engineer with a stable, high-paying job. They exhibit excellent spending discipline, consistently paying off their credit cards in full each month, resulting in a flawless credit history. Their existing debt is primarily a low-interest mortgage, well within their means to service. They have substantial savings and liquid assets, providing a strong financial safety net. Their request for a moderate personal loan for home renovations poses minimal risk. Their income stability, responsible debt behavior, and high overall financial health represent the ideal candidate.

## 2. Input Features Table

| Feature | Actual User Value | Category Range | Risk Interpretation | Backend Usage |
| ------- | ----------------- | -------------- | ------------------- | ------------- |
| Annual Income | ₹144,000 | > ₹100,000 | Excellent income capacity | Used as a primary normalizer for debt features |
| Monthly Income | ₹12,000 | > ₹8,000 | Steady cash flow | Baseline for DTI and affordability calculation |
| Existing Debt | ₹30,000 | Varies | Very manageable | Summed to calculate total outstanding obligations |
| Debt-to-Income Ratio (DTI) | 0.21 | 0.10–0.35 | Low risk of over-leverage | Core node in XGBoost split; passes business rule threshold |
| Credit Score | 790 | > 740 | Exceptional creditworthiness | Key feature; heavily weights the probability of default downward |
| Loan Amount Requested | ₹15,000 | Contextual | Modest relative to income | Compared against income limits and max exposure rules |
| Loan Tenure | 36 months | 12-60 months | Standard | Used to compute monthly EMI stress test |
| Employment Stability (years) | 6.0 | > 4.0 | Highly stable | Mitigates income volatility risk in the model |
| Savings Balance | ₹45,000 | > ₹20,000 | Strong buffer | Evaluated for liquidity coverage ratio |
| Monthly Expenses | ₹3,500 | Varies | Low overhead | Extracted for disposable income calculation |
| Credit Utilization Ratio | 8% | < 30% | Excellent credit management | Indicates user does not rely heavily on revolving credit |
| Number of Active Loans | 1 | 0-2 | Simplistic debt profile | Lower count correlates with lower aggregate default risk |
| Previous Loan Defaults | 0 | 0 | Perfect history | Hard constraint: >0 triggers instant rejection/review |
| Asset Value | ₹350,000 | > ₹100,000 | Substantial collateral/backing | Increases recovery probability estimation |
| Net Worth | ₹365,000 | Strongly Positive | High financial resilience | Secondary feature for extreme tail-risk mitigation |

## 3. Decision Pipeline

1. **Input Validation**: Pydantic schemas successfully validate all 15 inputs, ensuring strict type checking and range boundaries (e.g., DTI as a float, `Previous Loan Defaults` as an integer ≥ 0).
2. **Feature Engineering**: The service layer calculates derived metrics like `Disposable Income` (`Monthly Income` - `Monthly Expenses` - `EMI`) and normalizes categorical variables for the XGBoost pipeline.
3. **Model Interpretation**: The XGBoost model strongly favors the `Credit Score` (790) and `DTI` (0.21) features. The decision trees consistently route this data into low-risk leaf nodes, generating a negligible default probability.
4. **Estimated Default Probability**: 2.1%
5. **Final Backend Decision**: **Approved**
6. **Human-readable Explanation**: "Your loan application has been approved. Your excellent credit score and low debt-to-income ratio demonstrate a strong ability to manage additional credit successfully."

---

# User B: Medium Risk / Conditional Approval

## 1. Financial Scenario Description
User B is a mid-level marketing manager. While they have a steady income, they recently took out an auto loan and occasionally carry a balance on their credit cards, leading to some repayment stress indicators. Their savings are moderate, covering about two to three months of expenses. They are seeking a debt consolidation loan. While not highly risky, their current debt load requires careful underwriting and a higher interest rate or collateral requirement to mitigate risk. Their spending discipline is acceptable but leaves less room for error.

## 2. Input Features Table

| Feature | Actual User Value | Category Range | Risk Interpretation | Backend Usage |
| ------- | ----------------- | -------------- | ------------------- | ------------- |
| Annual Income | ₹72,000 | ₹50k–₹100k | Moderate income | Baseline for capacity limits |
| Monthly Income | ₹6,000 | ₹4k–₹8k | Sufficient but tight | Used to verify EMI serviceability |
| Existing Debt | ₹31,500 | Varies | Approaching limits | Aggregated for DTI constraints |
| Debt-to-Income Ratio (DTI) | 0.45 | 0.35–0.55 | Elevated risk of strain | Triggers secondary review; pushes XGBoost down higher-risk branches |
| Credit Score | 680 | 620–740 | Fair to Good | Neutral signal; requires other compensating factors |
| Loan Amount Requested | ₹10,000 | Contextual | Moderate | Used in post-approval affordability simulation |
| Loan Tenure | 48 months | 12-60 months | Extended | Increases total interest but lowers monthly EMI stress |
| Employment Stability (years) | 2.5 | 1.0-4.0 | Acceptable | Neutral factor in the model |
| Savings Balance | ₹8,500 | ₹5k–₹20k | Moderate buffer | Checked against minimum liquidity requirements |
| Monthly Expenses | ₹3,200 | Varies | Typical | Reduces available disposable income |
| Credit Utilization Ratio | 45% | 30%-60% | Moderate reliance | Slight negative weight in the model predictions |
| Number of Active Loans | 3 | 2-4 | Complex debt profile | Higher probability of overlapping payments |
| Previous Loan Defaults | 0 | 0 | Clean history | Passes business rule filter |
| Asset Value | ₹40,000 | ₹10k–₹100k | Limited collateral | Provides minor recovery offset |
| Net Worth | ₹17,000 | Positive | Marginal resilience | Indicates limited capacity to absorb financial shocks |

## 3. Decision Pipeline

1. **Input Validation**: Pydantic successfully parses the payload. No hard constraints are breached during the initial data validation phase.
2. **Feature Engineering**: The service layer flags the `Credit Utilization Ratio` (45%) and `DTI` (0.45) as elevated. A new synthetic feature, `Payment Stress Index`, is computed and fed into the model alongside raw inputs.
3. **Model Interpretation**: The XGBoost model detects interacting risks between the moderate `Credit Score` and the elevated `DTI`. However, the lack of previous defaults and positive `Net Worth` keep the prediction below the automatic rejection threshold.
4. **Estimated Default Probability**: 14.5%
5. **Final Backend Decision**: **Conditionally Approved** (Requires higher interest rate and direct payoff of consolidated debts)
6. **Human-readable Explanation**: "Your loan has been conditionally approved. While your payment history is clean, your current debt-to-income ratio is slightly elevated. We can offer you this loan at an adjusted rate to consolidate your existing obligations."

---

# User C: High Risk / Rejected

## 1. Financial Scenario Description
User C is a freelance graphic designer experiencing volatile income. They rely heavily on credit cards to cover daily expenses and have a history of late payments and a past default. Their existing debt burden is severe relative to their income, resulting in a very high DTI. They have no significant assets and negative net worth. Their request for a personal loan is highly risky, as they exhibit strong indicators of financial instability, lack of savings, and an inability to service new debt without compounding their financial stress.

## 2. Input Features Table

| Feature | Actual User Value | Category Range | Risk Interpretation | Backend Usage |
| ------- | ----------------- | -------------- | ------------------- | ------------- |
| Annual Income | ₹42,000 | < ₹50,000 | Low/Volatile | Restricts maximum allowable loan exposure |
| Monthly Income | ₹3,500 | < ₹4,000 | Constrained | Fails basic EMI affordability tests |
| Existing Debt | ₹25,000 | Varies | Disproportionately high | Triggers strict DTI circuit breakers |
| Debt-to-Income Ratio (DTI) | 0.62 | > 0.55 | Severe over-leverage | Hard business rule violation; extreme penalty in model |
| Credit Score | 580 | < 620 | Poor creditworthiness | Primary driver of high default probability |
| Loan Amount Requested | ₹8,000 | Contextual | High relative to income | Pushes projected DTI even higher |
| Loan Tenure | 24 months | 12-60 months | Short | Causes unaffordably high monthly EMI |
| Employment Stability (years) | 0.8 | < 1.0 | Highly unstable | Penalized by the model for income uncertainty |
| Savings Balance | ₹400 | < ₹2,000 | Inadequate buffer | Fails minimum liquidity business rule |
| Monthly Expenses | ₹2,800 | Varies | High overhead | Leaves virtually zero disposable income |
| Credit Utilization Ratio | 88% | > 60% | Maxed out credit | Indicates acute financial distress |
| Number of Active Loans | 5 | > 4 | Highly complex | Strong indicator of debt spiraling |
| Previous Loan Defaults | 1 | > 0 | Past failure | Frequently triggers automatic rejection |
| Asset Value | ₹5,000 | < ₹10,000 | Minimal | No significant recovery potential |
| Net Worth | -₹19,600 | Negative | Technically insolvent | Severe red flag in feature engineering phase |

## 3. Decision Pipeline

1. **Input Validation**: Pydantic receives the data. Although structurally valid types, the payload triggers early-warning flags in the validation layer for extreme values.
2. **Feature Engineering**: The service layer calculates a negative `Disposable Income`. The `Previous Loan Defaults` feature is mapped as a critical boolean flag, amplifying risk scores.
3. **Model Interpretation**: The XGBoost model heavily penalizes the combination of a 580 `Credit Score`, 0.62 `DTI`, and 88% `Credit Utilization`. The model places this user deep into the highest-risk terminal nodes, confirming severe repayment inability.
4. **Estimated Default Probability**: 68.2%
5. **Final Backend Decision**: **Rejected**
6. **Human-readable Explanation**: "We are unable to approve your loan application at this time. This decision is based on your highly elevated debt-to-income ratio, low credit score, and recent credit history. We recommend reducing existing balances before reapplying."

---

# Technical Notes

* **Why XGBoost performs well for structured financial data**: XGBoost excels at handling tabular data with complex, non-linear interactions. It inherently handles missing values, requires minimal scaling, and effectively models the non-linear relationship between compounding risk factors (e.g., how a low credit score exponentially worsens the risk of a high DTI).
* **How feature importance affects predictions**: The model relies on SHAP (SHapley Additive exPlanations) values to interpret feature importance. Features like `Credit Score` and `DTI` typically occupy the top nodes in the decision trees, meaning they dictate the broad direction of the prediction, while features like `Employment Stability` act as fine-tuning modifiers to the final probability.
* **Why DTI and credit score strongly influence outcomes**: DTI is a direct mathematical measure of current capacity, while the credit score is a historical measure of character and reliability. Combined, they form the most robust predictors of future behavior; thus, the training data naturally forces the algorithm to assign them the highest information gain.
* **How the backend combines ML predictions with business rules**: The system uses a hybrid approach. Hard business rules (e.g., `Previous Loan Defaults` > 0 or `DTI` > 0.60) can trigger immediate rejections (Circuit Breakers) regardless of the ML output. The ML model is primarily used for the vast "gray area" of users, providing a nuanced probability score that determines conditional approvals, interest rate adjustments, and manual review queues.

---

# Final Summary Table

| User | Risk Score | DTI | Credit Score | Net Worth | Predicted Default Probability | Final Loan Decision |
| ---- | ---------- | --- | ------------ | --------- | ----------------------------- | ------------------- |
| **User A** | Low | 0.21 | 790 | ₹365,000 | 2.1% | **Approved** |
| **User B** | Medium | 0.45 | 680 | ₹17,000 | 14.5% | **Conditionally Approved** |
| **User C** | High | 0.62 | 580 | -₹19,600 | 68.2% | **Rejected** |
