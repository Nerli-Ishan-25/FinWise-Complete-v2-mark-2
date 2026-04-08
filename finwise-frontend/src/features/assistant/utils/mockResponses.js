/**
 * mockResponses.js
 *
 * Simple keyword-based mock responses for the AI assistant.
 * Replace this with real API integration when backend is ready.
 */

export const MOCK_CONTEXT = {
  monthlyIncome:   5200,
  monthlyExpenses: 3100,
  savingsRate:     0.42,
  netWorth:        48500,
  assets:          62000,
  liabilities:     13500,
}

export function getMockResponse(query) {
  const q = query.toLowerCase()

  if (q.includes("dining") || q.includes("food") || q.includes("restaurant")) {
    return `**Food & Dining Analysis**

Based on your transaction history:

— Total dining spend: **$487** this month
— Up 12% from last month ($435)
— Average per transaction: $41
— 12 transactions recorded

⚠️ Your dining spend is 15% above the recommended 10% of income.

✅ Consider setting a $400 monthly limit to stay on track.`
  }

  if (q.includes("savings") || q.includes("rate")) {
    return `**Savings Rate Analysis**

Your current savings rate:

— **42%** of monthly income
— Last month: 38%
— Annual average: 40%

✅ Excellent! You're above the recommended 20% benchmark.

— Monthly surplus: $2,100
— Projected annual savings: $25,200`
  }

  if (q.includes("summary") || q.includes("overview")) {
    return `**Monthly Summary · March 2026**

**Income & Expenses**

— Income: $5,200 (+3% vs Feb)
— Expenses: $3,100 (+8% vs Feb)
— Net: +$2,100

**Top Spending Categories**

— Housing: $1,400 (45% of expenses)
— Food & Dining: $487 (16%)
— Transportation: $320 (10%)
— Entertainment: $280 (9%)

**Net Worth Change**

— Current: $48,500
— Last month: $46,800
— Change: +$1,700 (+3.6%)

✅ You're on track with your financial goals.`
  }

  if (q.includes("budget") || q.includes("suggest")) {
    return `**Budget Suggestions**

Based on your spending patterns:

**Recommended Monthly Limits**

— Food & Dining: $400 (current: $487)
— Entertainment: $250 (current: $280)
— Shopping: $200 (current: $180) ✅
— Transportation: $350 (current: $320) ✅

**Action Items**

— Reduce dining out by 2-3 meals/month
— Set entertainment budget alert at $200
— Consider meal prep to save ~$100/month

⚠️ Small adjustments could save $150-200/month.`
  }

  if (q.includes("anomal") || q.includes("unusual") || q.includes("abnormal")) {
    return `**Spending Anomalies Detected**

Found 3 unusual transactions:

— **$289** at TechStore Inc (Mar 18)
  · 3.2x above your electronics avg
— **$156** at Restaurant XYZ (Mar 12)
  · 2.1x above your dining avg
— **$89** at Coffee Shop (Mar 8)
  · 4x above your coffee avg

⚠️ Review these transactions for potential errors or fraud.

✅ Set up transaction alerts for amounts >$200.`
  }

  if (q.includes("track") || q.includes("goal") || q.includes("annual")) {
    return `**Annual Goals Progress**

**2026 Financial Goals**

✅ Emergency Fund: $15,000 / $20,000 (75%)
— On track to complete by Q3

⚠️ Investment Portfolio: $28,000 / $50,000 (56%)
— Need $1,850/month to reach goal

✅ Debt Reduction: $3,200 / $10,000 (32%)
— Ahead of schedule by 2 months

**Recommendation**

Increase investment contribution by $400/month to stay on track.`
  }

  // Default fallback response
  return `**Analysis Complete**

I've reviewed your financial data:

**Key Metrics**

— Monthly Income: $5,200
— Monthly Expenses: $3,100
— Savings Rate: 42%
— Net Worth: $48,500

**Quick Insights**

— Your savings rate is excellent (42% vs 20% recommended)
— Food spending is slightly elevated this month
— Net worth grew by $1,700 this month

Ask me about specific categories or trends for deeper analysis.`
}
