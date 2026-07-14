using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class AuthApiService
    {
        private readonly HttpClient _httpClient;

        public AuthApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<Token?> LoginAsync(string username, string password)
        {
            var request = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("username", username),
                new KeyValuePair<string, string>("password", password)
            });

            var response = await _httpClient.PostAsync("auth/login", request);
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadFromJsonAsync<Token>();
        }

        public async Task<UserInDB?> GetProfileAsync()
        {
            var response = await _httpClient.GetAsync("finance/profile");
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadFromJsonAsync<UserInDB>();
        }
    }
}
