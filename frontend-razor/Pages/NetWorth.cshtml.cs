using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using FinWise.Razor.Services;
using FinWise.Razor.Models.DTOs;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace FinWise.Razor.Pages
{
    public class NetWorthModel : PageModel
    {
        private readonly AssetApiService _assetService;
        private readonly LiabilityApiService _liabilityService;

        public NetWorthModel(AssetApiService assetService, LiabilityApiService liabilityService)
        {
            _assetService = assetService;
            _liabilityService = liabilityService;
        }

        public List<AssetResponse> Assets { get; set; } = new();
        public List<LiabilityResponse> Liabilities { get; set; } = new();

        public double TotalAssets => Assets.Sum(a => a.Value);
        public double TotalLiabilities => Liabilities.Sum(l => l.Amount);
        public double NetWorth => TotalAssets - TotalLiabilities;

        [BindProperty]
        public AssetCreate AssetInput { get; set; } = new();

        [BindProperty]
        public LiabilityCreate LiabilityInput { get; set; } = new();

        public async Task<IActionResult> OnGetAsync()
        {
            try
            {
                Assets = await _assetService.GetAssetsAsync();
                Liabilities = await _liabilityService.GetLiabilitiesAsync();
            }
            catch { /* Backend offline — render with empty data */ }
            return Page();
        }

        public async Task<IActionResult> OnPostAddAssetAsync()
        {
            if (AssetInput.Value > 0 && !string.IsNullOrEmpty(AssetInput.Name))
            {
                await _assetService.CreateAssetAsync(AssetInput);
            }
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostDeleteAssetAsync(int id)
        {
            await _assetService.DeleteAssetAsync(id);
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostAddLiabilityAsync()
        {
            if (LiabilityInput.Amount > 0 && !string.IsNullOrEmpty(LiabilityInput.Name))
            {
                await _liabilityService.CreateLiabilityAsync(LiabilityInput);
            }
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostDeleteLiabilityAsync(int id)
        {
            await _liabilityService.DeleteLiabilityAsync(id);
            return RedirectToPage();
        }
    }
}
