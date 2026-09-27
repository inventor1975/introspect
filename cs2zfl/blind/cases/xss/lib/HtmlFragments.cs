using System.Text.Encodings.Web;

namespace Storefront.Web.Markup
{
    public static class HtmlFragments
    {
        public static string Paragraph(string text)
        {
            return "<p class=\"note\">" + text + "</p>";
        }

        public static string EncodedParagraph(string text)
        {
            return "<p class=\"note\">" + HtmlEncoder.Default.Encode(text) + "</p>";
        }

        public static string Heading(int level, string text)
        {
            var lvl = level < 1 || level > 6 ? 2 : level;
            return $"<h{lvl}>{text}</h{lvl}>";
        }

        public static string Document(string title, string body)
        {
            return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>Storefront</title></head><body>"
                + body + "</body></html>";
        }
    }
}
