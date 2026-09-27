using System.Net;

namespace Storefront.Web.Markup
{
    public interface IMarkupRenderer
    {
        string RenderMessage(string message);
    }

    public sealed class PlainMarkupRenderer : IMarkupRenderer
    {
        public string RenderMessage(string message) => $"<div class=\"msg\">{message}</div>";
    }

    public sealed class EscapingMarkupRenderer : IMarkupRenderer
    {
        public string RenderMessage(string message) => $"<div class=\"msg\">{WebUtility.HtmlEncode(message)}</div>";
    }
}
