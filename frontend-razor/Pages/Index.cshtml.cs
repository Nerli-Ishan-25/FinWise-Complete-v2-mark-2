using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using FinWise.Razor.Services;
using FinWise.Razor.Models.DTOs;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json;

namespace FinWise.Razor.Pages
{
    public class IndexModel : PageModel
    {
        private readonly DashboardApiService _dashboardService;
        private readonly ExpenseApiService _expenseService;

        public IndexModel(DashboardApiService dashboardService, ExpenseApiService expenseService)
        {
            _dashboardService = dashboardService;
            _expenseService = expenseService;
        }

        public DashboardMetrics? Metrics { get; set; }
        public List<MonthlySummaryItem> MonthlySummary { get; set; } = new();
        public List<TransactionResponse> RecentTransactions { get; set; } = new();

        public string ChartLabelsJson { get; set; } = "[]";
        public string IncomeDataJson { get; set; } = "[]";
        public string ExpensesDataJson { get; set; } = "[]";

        public async Task<IActionResult> OnGetAsync()
        {
            try
            {
                Metrics = await _dashboardService.GetDashboardMetricsAsync();
                MonthlySummary = await _dashboardService.GetMonthlySummaryAsync(6);

                var allTx = await _expenseService.GetTransactionsAsync();
                RecentTransactions = allTx.OrderByDescending(t => t.Date).Take(5).ToList();

                if (MonthlySummary.Any())
                {
                    var ordered = MonthlySummary.ToList();
                    ChartLabelsJson = JsonSerializer.Serialize(ordered.Select(m => m.Month));
                    IncomeDataJson = JsonSerializer.Serialize(ordered.Select(m => m.Income));
                    ExpensesDataJson = JsonSerializer.Serialize(ordered.Select(m => m.Expense));
                }
            }
            catch
            {
                // Ignore API failures for pure UI preview
            }

            return Page();
        }
    }
}
