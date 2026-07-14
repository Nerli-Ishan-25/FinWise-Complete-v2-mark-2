using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class AssetApiService
    {
        private readonly HttpClient _httpClient;

        public AssetApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<AssetResponse>> GetAssetsAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<AssetResponse>>("assets/") ?? new List<AssetResponse>();
        }

        public async Task<AssetResponse?> CreateAssetAsync(AssetCreate asset)
        {
            var response = await _httpClient.PostAsJsonAsync("assets/", asset);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<AssetResponse>();
        }

        public async Task<AssetResponse?> UpdateAssetAsync(int id, AssetUpdate asset)
        {
            var response = await _httpClient.PutAsJsonAsync($"assets/{id}", asset);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<AssetResponse>();
        }

        public async Task<bool> DeleteAssetAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"assets/{id}");
            return response.IsSuccessStatusCode;
        }
    }
}
