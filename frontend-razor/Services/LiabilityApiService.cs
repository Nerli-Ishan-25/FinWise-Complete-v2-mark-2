using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class LiabilityApiService
    {
        private readonly HttpClient _httpClient;

        public LiabilityApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<LiabilityResponse>> GetLiabilitiesAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<LiabilityResponse>>("liabilities/") ?? new List<LiabilityResponse>();
        }

        public async Task<LiabilityResponse?> CreateLiabilityAsync(LiabilityCreate liability)
        {
            var response = await _httpClient.PostAsJsonAsync("liabilities/", liability);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<LiabilityResponse>();
        }

        public async Task<LiabilityResponse?> UpdateLiabilityAsync(int id, LiabilityUpdate liability)
        {
            var response = await _httpClient.PutAsJsonAsync($"liabilities/{id}", liability);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<LiabilityResponse>();
        }

        public async Task<bool> DeleteLiabilityAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"liabilities/{id}");
            return response.IsSuccessStatusCode;
        }
    }
}
