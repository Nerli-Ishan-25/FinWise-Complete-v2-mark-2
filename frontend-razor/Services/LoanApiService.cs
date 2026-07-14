using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class LoanApiService
    {
        private readonly HttpClient _httpClient;

        public LoanApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<LoanResponse>> GetLoansAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<LoanResponse>>("finance/loans") ?? new List<LoanResponse>();
        }

        public async Task<LoanAssessmentResponse?> PredictLoanAsync(LoanAssessmentRequest request)
        {
            var response = await _httpClient.PostAsJsonAsync("loan-assessment/predict", request);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<LoanAssessmentResponse>();
        }
    }
}
