using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Rendering;

namespace Storefront.Components
{
    [Route("/notice")]
    public class AnnouncementText : ComponentBase
    {
        [SupplyParameterFromQuery(Name = "text")]
        public string? Text { get; set; }

        private static readonly MarkupString Icon = new MarkupString("<svg class=\"icon\"><use href=\"#megaphone\"/></svg>");

        protected override void BuildRenderTree(RenderTreeBuilder builder)
        {
            builder.OpenElement(0, "div");
            builder.AddAttribute(1, "class", "announcement");
            builder.AddContent(2, Icon);
            builder.AddContent(3, Text ?? string.Empty);
            builder.CloseElement();
        }
    }
}
