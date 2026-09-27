using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Rendering;

namespace Storefront.Components
{
    [Route("/announce")]
    public class AnnouncementBar : ComponentBase
    {
        [SupplyParameterFromQuery(Name = "text")]
        public string? Text { get; set; }

        protected override void BuildRenderTree(RenderTreeBuilder builder)
        {
            builder.OpenElement(0, "div");
            builder.AddAttribute(1, "class", "announcement");
            builder.AddContent(2, (MarkupString)(Text ?? string.Empty));
            builder.CloseElement();
        }
    }
}
