using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class BudgetApiService
    {
        private readonly HttpClient _httpClient;

        public BudgetApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<BudgetResponse>> GetBudgetsAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<BudgetResponse>>("budgets/") ?? new List<BudgetResponse>();
        }

        public async Task<BudgetResponse?> CreateBudgetAsync(BudgetCreate budget)
        {
            var response = await _httpClient.PostAsJsonAsync("budgets/", budget);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<BudgetResponse>();
        }

        public async Task<BudgetResponse?> UpdateBudgetAsync(int id, BudgetUpdate budget)
        {
            var response = await _httpClient.PutAsJsonAsync($"budgets/{id}", budget);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<BudgetResponse>();
        }

        public async Task<bool> DeleteBudgetAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"budgets/{id}");
            return response.IsSuccessStatusCode;
        }
    }
}
