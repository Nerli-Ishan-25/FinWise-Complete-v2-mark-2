using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class DashboardApiService
    {
        private readonly HttpClient _httpClient;

        public DashboardApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<DashboardMetrics?> GetDashboardMetricsAsync()
        {
            return await _httpClient.GetFromJsonAsync<DashboardMetrics>("finance/dashboard");
        }

        public async Task<List<MonthlySummaryItem>> GetMonthlySummaryAsync(int months = 7)
        {
            return await _httpClient.GetFromJsonAsync<List<MonthlySummaryItem>>($"finance/monthly-summary?months={months}") ?? new List<MonthlySummaryItem>();
        }
    }
}
