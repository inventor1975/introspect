using System.Text;

namespace Storefront.Web.Markup
{
    public sealed class PageBuilder
    {
        private readonly StringBuilder _body = new StringBuilder();
        private string _title = "Untitled";

        public PageBuilder Title(string title)
        {
            _title = title;
            return this;
        }

        public PageBuilder Section(string heading, string content)
        {
            _body.Append("<section><h2>").Append(heading).Append("</h2>");
            _body.Append("<div>").Append(content).Append("</div></section>");
            return this;
        }

        public string Build()
        {
            return $"<!DOCTYPE html><html><head><title>{_title}</title></head><body>{_body}</body></html>";
        }
    }
}
