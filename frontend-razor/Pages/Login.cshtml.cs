using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;
using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using FinWise.Razor.Services;

namespace FinWise.Razor.Pages
{
    public class LoginModel : PageModel
    {
        private readonly AuthApiService _authService;

        public LoginModel(AuthApiService authService)
        {
            _authService = authService;
        }

        [BindProperty]
        public InputModel Input { get; set; } = new();

        public class InputModel
        {
            [Required]
            [EmailAddress]
            public string Email { get; set; } = string.Empty;

            [Required]
            [DataType(DataType.Password)]
            public string Password { get; set; } = string.Empty;
        }

        [TempData]
        public string? ErrorMessage { get; set; }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            try
            {
                var token = await _authService.LoginAsync(Input.Email, Input.Password);
                if (token != null && !string.IsNullOrEmpty(token.AccessToken))
                {
                    var claims = new List<Claim>
                    {
                        new Claim(ClaimTypes.Name, Input.Email),
                        new Claim(ClaimTypes.Email, Input.Email)
                    };

                    var claimsIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);

                    var authProperties = new AuthenticationProperties
                    {
                        IsPersistent = true
                    };

                    authProperties.StoreTokens(new[] {
                        new AuthenticationToken { Name = "access_token", Value = token.AccessToken }
                    });

                    await HttpContext.SignInAsync(
                        CookieAuthenticationDefaults.AuthenticationScheme, 
                        new ClaimsPrincipal(claimsIdentity), 
                        authProperties);

                    return RedirectToPage("/Index");
                }
                
                ErrorMessage = "Invalid login attempt.";
                return Page();
            }
            catch (Exception)
            {
                ErrorMessage = "An error occurred during login. Please verify your credentials.";
                return Page();
            }
        }
    }
}
