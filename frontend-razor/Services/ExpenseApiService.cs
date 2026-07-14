using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class ExpenseApiService
    {
        private readonly HttpClient _httpClient;

        public ExpenseApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<ExpenseResponse>> GetExpensesAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<ExpenseResponse>>("finance/expenses") ?? new List<ExpenseResponse>();
        }

        public async Task<List<TransactionResponse>> GetTransactionsAsync(int limit = 50)
        {
            return await _httpClient.GetFromJsonAsync<List<TransactionResponse>>($"finance/transactions?limit={limit}") ?? new List<TransactionResponse>();
        }

        public async Task<ExpenseResponse?> CreateExpenseAsync(ExpenseCreate expense)
        {
            var response = await _httpClient.PostAsJsonAsync("finance/expenses", expense);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<ExpenseResponse>();
        }

        public async Task<IncomeResponse?> CreateIncomeAsync(IncomeCreate income)
        {
            var response = await _httpClient.PostAsJsonAsync("finance/income", income);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<IncomeResponse>();
        }

        public async Task<bool> DeleteTransactionAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"finance/transactions/{id}");
            return response.IsSuccessStatusCode;
        }
    }
}
