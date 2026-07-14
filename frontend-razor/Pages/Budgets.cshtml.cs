using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using FinWise.Razor.Services;
using FinWise.Razor.Models.DTOs;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System;

namespace FinWise.Razor.Pages
{
    public class BudgetsModel : PageModel
    {
        private readonly BudgetApiService _budgetService;
        private readonly CategoryApiService _categoryService;

        public BudgetsModel(BudgetApiService budgetService, CategoryApiService categoryService)
        {
            _budgetService = budgetService;
            _categoryService = categoryService;
        }

        public List<BudgetResponse> Budgets { get; set; } = new();
        public List<CategoryResponse> Categories { get; set; } = new();

        [BindProperty]
        public BudgetInputModel Input { get; set; } = new();

        public class BudgetInputModel
        {
            public int CategoryId { get; set; }
            public double BudgetAmount { get; set; }
            public int Month { get; set; } = DateTime.Today.Month;
            public int Year { get; set; } = DateTime.Today.Year;
        }

        public async Task<IActionResult> OnGetAsync()
        {
            try { await LoadDataAsync(); }
            catch { /* Backend offline — render with empty data */ }
            return Page();
        }

        private async Task LoadDataAsync()
        {
            Budgets = await _budgetService.GetBudgetsAsync();
            Categories = await _categoryService.GetCategoriesAsync();
            
            // Filter to only Expense categories for budgeting
            Categories = Categories.Where(c => c.Type.ToLower() == "expense").ToList();
        }

        public async Task<IActionResult> OnPostAddBudgetAsync()
        {
            if (Input.BudgetAmount <= 0)
            {
                ModelState.AddModelError(string.Empty, "Amount must be greater than zero.");
                await LoadDataAsync();
                return Page();
            }

            var createReq = new BudgetCreate
            {
                CategoryId = Input.CategoryId,
                BudgetAmount = Input.BudgetAmount,
                Month = Input.Month,
                Year = Input.Year
            };

            await _budgetService.CreateBudgetAsync(createReq);
            return RedirectToPage();
        }
        
        public async Task<IActionResult> OnPostEditBudgetAsync(int id, double amount)
        {
            if (amount <= 0)
            {
                return RedirectToPage(); // Optionally add error handling
            }

            var updateReq = new BudgetUpdate
            {
                BudgetAmount = amount
            };

            await _budgetService.UpdateBudgetAsync(id, updateReq);
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostDeleteBudgetAsync(int id)
        {
            await _budgetService.DeleteBudgetAsync(id);
            return RedirectToPage();
        }
    }
}
