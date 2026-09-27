using System;
using System.Text.RegularExpressions;

namespace Storefront.Web.Validation
{
    public static class InputRules
    {
        private static readonly Regex SlugPattern = new Regex("^[a-z0-9-]{1,48}$", RegexOptions.Compiled);
        private static readonly Regex WordPattern = new Regex("[A-Za-z]+", RegexOptions.Compiled);

        public static bool IsSlug(string value) => value != null && SlugPattern.IsMatch(value);

        public static bool HasLetters(string value) => value != null && WordPattern.IsMatch(value);

        public static string StripScriptTags(string value)
        {
            if (string.IsNullOrEmpty(value)) return string.Empty;
            return value.Replace("<script>", string.Empty, StringComparison.OrdinalIgnoreCase)
                        .Replace("</script>", string.Empty, StringComparison.OrdinalIgnoreCase);
        }

        public static string Truncate(string value, int max)
        {
            if (value == null) return string.Empty;
            return value.Length <= max ? value : value.Substring(0, max);
        }
    }
}
