using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace FinWise.Razor.Models.DTOs
{
    public enum UserRole
    {
        [JsonPropertyName("admin")]
        Admin,
        [JsonPropertyName("user")]
        User
    }

    public class UserBase
    {
        public string Name { get; set; } = string.Empty;
        
        [EmailAddress]
        public string Email { get; set; } = string.Empty;
        
        public UserRole? Role { get; set; } = UserRole.User;
    }

    public class UserCreate : UserBase
    {
        [MaxLength(72)]
        public string Password { get; set; } = string.Empty;
    }

    public class UserUpdate
    {
        public string? Name { get; set; }
        
        [EmailAddress]
        public string? Email { get; set; }
        
        public UserRole? Role { get; set; }
    }

    public class UserInDB : UserBase
    {
        public int Id { get; set; }
        
        public DateTime CreatedAt { get; set; }
        
        public bool Onboarded { get; set; } = false;
    }

    public class Token
    {
        [JsonPropertyName("access_token")]
        public string AccessToken { get; set; } = string.Empty;
        
        [JsonPropertyName("token_type")]
        public string TokenType { get; set; } = string.Empty;
    }

    public class TokenData
    {
        public string? Id { get; set; }
        public string? Email { get; set; }
        public string? Role { get; set; }
    }

    public class OnboardingData
    {
        public string Goal { get; set; } = string.Empty;
        public List<AssetCreate> Assets { get; set; } = new();
        public List<LiabilityCreate> Liabilities { get; set; } = new();
        public List<IncomeCreate> Income { get; set; } = new();
    }
}
