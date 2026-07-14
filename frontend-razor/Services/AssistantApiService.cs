using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FinWise.Razor.Models.DTOs;

namespace FinWise.Razor.Services
{
    public class AssistantApiService
    {
        private readonly HttpClient _httpClient;

        public AssistantApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<ChatResponse?> SendMessageAsync(ChatRequest request)
        {
            var response = await _httpClient.PostAsJsonAsync("assistant/chat", request);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<ChatResponse>();
        }
    }
}
