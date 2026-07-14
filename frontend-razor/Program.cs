using Microsoft.AspNetCore.Authentication.Cookies;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages(options =>
{
    // options.Conventions.AuthorizeFolder("/");
    options.Conventions.AllowAnonymousToPage("/Login");
    options.Conventions.AllowAnonymousToPage("/Register");
});

builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        options.LoginPath = "/Login";
        options.LogoutPath = "/Logout";
        options.AccessDeniedPath = "/AccessDenied";
    });

builder.Services.AddHttpContextAccessor();
builder.Services.AddTransient<FinWise.Razor.Services.TokenAuthHandler>();

var apiBaseUrl = builder.Configuration["ApiBaseUrl"] ?? "http://localhost:8000/api/v1/";

builder.Services.AddHttpClient<FinWise.Razor.Services.AuthApiService>(client => client.BaseAddress = new Uri(apiBaseUrl));
// We do not add the TokenAuthHandler to AuthApiService because it doesn't need to send tokens for login, but it might need it for GetProfile. Actually, GetProfile needs it. 
// However, TokenAuthHandler requires HttpContext. If we add it, it'll just send null if no token is available, which is fine.
builder.Services.AddHttpClient<FinWise.Razor.Services.AuthApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.ExpenseApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.BudgetApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.CategoryApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.AssetApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.LiabilityApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.DashboardApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.LoanApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();
builder.Services.AddHttpClient<FinWise.Razor.Services.AssistantApiService>(client => client.BaseAddress = new Uri(apiBaseUrl))
    .AddHttpMessageHandler<FinWise.Razor.Services.TokenAuthHandler>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();
