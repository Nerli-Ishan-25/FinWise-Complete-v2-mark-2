using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using FinWise.Razor.Services;
using FinWise.Razor.Models.DTOs;
using System.Text.Json;
using System.Globalization;
using System.Collections.Generic;
using System.Linq;
using System;
using System.Threading.Tasks;

namespace FinWise.Razor.Pages
{
    public class ExpensesModel : PageModel
    {
        private readonly ExpenseApiService _expenseService;

        public ExpensesModel(ExpenseApiService expenseService)
        {
            _expenseService = expenseService;
        }

        public List<TransactionResponse> Transactions { get; set; } = new();
        public string MonthlyTrendsJson { get; set; } = "[]";
        public string CategorySpendingJson { get; set; } = "[]";
        public List<CategorySpending> CategorySpendingList { get; set; } = new();

        [BindProperty]
        public TransactionInputModel Input { get; set; } = new();

        public class TransactionInputModel
        {
            public string Description { get; set; } = string.Empty;
            public double Amount { get; set; }
            public string Type { get; set; } = "expense";
            public string Category { get; set; } = "Food";
            public DateTime Date { get; set; } = DateTime.Today;
        }
        
        public class CategorySpending
        {
            public string Name { get; set; } = string.Empty;
            public double Value { get; set; }
            public string Color { get; set; } = string.Empty;
        }

        public async Task<IActionResult> OnGetAsync()
        {
            try { await LoadDataAsync(); }
            catch { /* Backend offline — render with empty data */ }
            return Page();
        }

        private async Task LoadDataAsync()
        {
            Transactions = await _expenseService.GetTransactionsAsync(100);

            // Calculate Monthly Trends
            var monthlyTrendsMap = new Dictionary<string, MonthlyTrendData>();
            foreach (var tx in Transactions)
            {
                var date = tx.Date;
                var key = $"{date.Year}-{date.Month:D2}";
                if (!monthlyTrendsMap.ContainsKey(key))
                {
                    monthlyTrendsMap[key] = new MonthlyTrendData { Key = key, Month = date.ToString("MMM", CultureInfo.InvariantCulture), Income = 0, Expense = 0 };
                }
                
                if (tx.Type.ToLower() == "income")
                    monthlyTrendsMap[key].Income += tx.Amount;
                else
                    monthlyTrendsMap[key].Expense += tx.Amount;
            }

            var trends = monthlyTrendsMap.Values
                .OrderBy(x => x.Key)
                .TakeLast(7)
                .Select(x => new { m = x.Month, income = x.Income, expense = x.Expense })
                .ToList();
            
            MonthlyTrendsJson = JsonSerializer.Serialize(trends);

            // Calculate Spending By Category
            var categoryMap = new Dictionary<string, double>();
            foreach (var tx in Transactions.Where(t => t.Type.ToLower() == "expense"))
            {
                var cat = string.IsNullOrEmpty(tx.Category) ? "Other" : tx.Category;
                if (!categoryMap.ContainsKey(cat))
                    categoryMap[cat] = 0;
                categoryMap[cat] += tx.Amount;
            }

            var categoryColors = new Dictionary<string, string>
            {
                {"Housing", "#448aff"}, {"Food", "#00e676"}, {"Transport", "#ffab40"},
                {"Subscriptions", "#b388ff"}, {"Entertainment", "#ff5252"},
                {"Health", "#40c4ff"}, {"Income", "#64ffda"}, {"Other", "#ff80ab"},
                {"Shopping", "#f06292"}, {"Utilities", "#9575cd"}, {"Investments", "#81c784"}
            };

            CategorySpendingList = categoryMap.Select(kv => new CategorySpending
            {
                Name = kv.Key,
                Value = Math.Round(kv.Value, 2),
                Color = categoryColors.ContainsKey(kv.Key) ? categoryColors[kv.Key] : "#cccccc"
            }).OrderByDescending(x => x.Value).ToList();

            var catsForJson = CategorySpendingList.Select(x => new { name = x.Name, value = x.Value, color = x.Color }).ToList();
            CategorySpendingJson = JsonSerializer.Serialize(catsForJson);
        }

        public async Task<IActionResult> OnPostAddTransactionAsync()
        {
            if (!ModelState.IsValid)
            {
                await LoadDataAsync();
                return Page();
            }

            if (Input.Type == "income")
            {
                var income = new IncomeCreate
                {
                    Amount = Input.Amount,
                    Source = Input.Description,
                    Date = Input.Date
                };
                await _expenseService.CreateIncomeAsync(income);
            }
            else
            {
                var expense = new ExpenseCreate
                {
                    Amount = Input.Amount,
                    Description = Input.Description,
                    Category = Input.Category,
                    Date = Input.Date
                };
                await _expenseService.CreateExpenseAsync(expense);
            }
            
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostDeleteTransactionAsync(int id)
        {
            await _expenseService.DeleteTransactionAsync(id);
            return RedirectToPage();
        }

        class MonthlyTrendData
        {
            public string Key { get; set; } = string.Empty;
            public string Month { get; set; } = string.Empty;
            public double Income { get; set; }
            public double Expense { get; set; }
        }
    }
}
