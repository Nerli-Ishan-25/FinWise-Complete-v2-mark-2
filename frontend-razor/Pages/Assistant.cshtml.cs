using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using FinWise.Razor.Services;
using FinWise.Razor.Models.DTOs;
using System.Threading.Tasks;
using System;

namespace FinWise.Razor.Pages
{
    [IgnoreAntiforgeryToken] // Allow simple fetch from JS
    public class AssistantModel : PageModel
    {
        private readonly AssistantApiService _assistantService;

        public AssistantModel(AssistantApiService assistantService)
        {
            _assistantService = assistantService;
        }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPostSendMessageAsync([FromBody] ChatRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Message))
            {
                return BadRequest("Message is empty");
            }

            try
            {
                var response = await _assistantService.SendMessageAsync(request);
                return new JsonResult(response);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = "Failed to communicate with AI Assistant." });
            }
        }
    }
}
