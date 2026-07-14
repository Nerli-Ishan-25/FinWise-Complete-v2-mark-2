using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class CategoryApiService
    {
        private readonly HttpClient _httpClient;

        public CategoryApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<CategoryResponse>> GetCategoriesAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<CategoryResponse>>("categories/") ?? new List<CategoryResponse>();
        }

        public async Task<CategoryResponse?> CreateCategoryAsync(CategoryCreate category)
        {
            var response = await _httpClient.PostAsJsonAsync("categories/", category);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<CategoryResponse>();
        }

        public async Task<bool> DeleteCategoryAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"categories/{id}");
            return response.IsSuccessStatusCode;
        }
    }
}
