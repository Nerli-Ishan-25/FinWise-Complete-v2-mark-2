using System;
using System.Collections.Generic;

namespace FinWise.Razor.Models.DTOs
{
    public class FinanceBase
    {
        public double Amount { get; set; }
        public DateTime? Date { get; set; }
    }

    public class IncomeCreate : FinanceBase
    {
        public string Source { get; set; } = string.Empty;
        public string? Description { get; set; }
    }

    public class IncomeResponse : FinanceBase
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Source { get; set; } = string.Empty;
        public string? Description { get; set; }
    }

    public class ExpenseCreate : FinanceBase
    {
        public string Category { get; set; } = string.Empty;
        public string? Description { get; set; }
    }

    public class ExpenseResponse : FinanceBase
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Category { get; set; } = string.Empty;
        public string? Description { get; set; }
    }

    public class LoanCreate
    {
        public double LoanAmount { get; set; }
        public double InterestRate { get; set; }
        public double RemainingAmount { get; set; }
    }

    public class LoanResponse : LoanCreate
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class DashboardMetrics
    {
        public double NetWorth { get; set; }
        public double MonthlyIncome { get; set; }
        public double MonthlyExpenses { get; set; }
        public double SavingsRate { get; set; }
        public double FinancialHealthScore { get; set; }
        public List<string> Insights { get; set; } = new();
        public double? ForecastedNextMonth { get; set; }
    }

    public class TransactionResponse
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Type { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public double Amount { get; set; }
        public DateTime Date { get; set; }
        public string? Description { get; set; }
    }

    public class MonthlySummaryItem
    {
        public string Month { get; set; } = string.Empty;
        public double Income { get; set; }
        public double Expense { get; set; }
    }

    public class AssetCreate
    {
        public string Name { get; set; } = string.Empty;
        public string? Type { get; set; }
        public double Value { get; set; }
    }

    public class AssetUpdate
    {
        public string? Name { get; set; }
        public string? Type { get; set; }
        public double? Value { get; set; }
    }

    public class AssetResponse
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Name { get; set; } = string.Empty;
        public string? Type { get; set; }
        public double Value { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class LiabilityCreate
    {
        public string Name { get; set; } = string.Empty;
        public string? Type { get; set; }
        public double Amount { get; set; }
        public double InterestRate { get; set; }
    }

    public class LiabilityUpdate
    {
        public string? Name { get; set; }
        public string? Type { get; set; }
        public double? Amount { get; set; }
        public double? InterestRate { get; set; }
    }

    public class LiabilityResponse
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Name { get; set; } = string.Empty;
        public string? Type { get; set; }
        public double Amount { get; set; }
        public double InterestRate { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class CategoryCreate
    {
        public string Name { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
    }

    public class CategoryResponse
    {
        public int Id { get; set; }
        public int? UserId { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
    }

    public class BudgetCreate
    {
        public int CategoryId { get; set; }
        public double BudgetAmount { get; set; }
        public int Month { get; set; }
        public int Year { get; set; }
    }

    public class BudgetUpdate
    {
        public double BudgetAmount { get; set; }
    }

    public class BudgetResponse
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public int? CategoryId { get; set; }
        public double BudgetAmount { get; set; }
        public int Month { get; set; }
        public int Year { get; set; }
        public string? CategoryName { get; set; }
        public double Spent { get; set; } = 0.0;
    }

    public class SubscriptionCreate
    {
        public string Name { get; set; } = string.Empty;
        public double Amount { get; set; }
        public string BillingCycle { get; set; } = string.Empty;
        public DateTime NextPaymentDate { get; set; }
        public bool? Active { get; set; } = true;
        public DateTime? LastUsed { get; set; }
    }

    public class SubscriptionUpdate
    {
        public string? Name { get; set; }
        public double? Amount { get; set; }
        public string? BillingCycle { get; set; }
        public DateTime? NextPaymentDate { get; set; }
        public bool? Active { get; set; }
        public DateTime? LastUsed { get; set; }
    }

    public class SubscriptionResponse
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Name { get; set; } = string.Empty;
        public double Amount { get; set; }
        public string BillingCycle { get; set; } = string.Empty;
        public DateTime? NextPaymentDate { get; set; }
        public bool? Active { get; set; } = true;
        public DateTime? LastUsed { get; set; }
    }

    public class IncomeUpdateRequest
    {
        public double Income { get; set; }
    }

    public class LoanAssessmentRequest
    {
        public int Age { get; set; }
        public double Income { get; set; }
        public int CreditScore { get; set; }
        public int MonthsEmployed { get; set; }
        public int NumCreditLines { get; set; }
        
        public string Education { get; set; } = string.Empty;
        public string EmploymentType { get; set; } = string.Empty;
        public string MaritalStatus { get; set; } = string.Empty;
        public string HasMortgage { get; set; } = string.Empty;
        public string HasDependents { get; set; } = string.Empty;
        public string HasCoSigner { get; set; } = string.Empty;
        
        public double LoanAmount { get; set; }
        public int LoanTerm { get; set; }
        public string LoanPurpose { get; set; } = string.Empty;
        public double InterestRate { get; set; } = 7.0;
        public double ExistingDebt { get; set; }
    }

    public class LoanAssessmentResponse
    {
        public bool Eligible { get; set; }
        public double DefaultProbability { get; set; }
        public double DefaultProbabilityPct { get; set; }
        public double ThresholdUsed { get; set; }
        public string RiskLevel { get; set; } = string.Empty;
        public double ConfidencePct { get; set; }
        public string Explanation { get; set; } = string.Empty;
        public List<string> KeyFactors { get; set; } = new();
        public double MonthlyPayment { get; set; }
        public double DebtToIncomeRatio { get; set; }
        public double TotalInterest { get; set; }
    }

    public class ChatRequest
    {
        public string Message { get; set; } = string.Empty;
        public List<ChatMessage> History { get; set; } = new();
    }

    public class ChatMessage
    {
        public string Role { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
    }

    public class ChatResponse
    {
        public string Reply { get; set; } = string.Empty;
    }
}
