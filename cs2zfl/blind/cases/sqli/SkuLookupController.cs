using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("catalog/sku")]
    public class SkuLookupController : Controller
    {
        private readonly CatalogRepository _catalog;

        public SkuLookupController(CatalogRepository catalog)
        {
            _catalog = catalog;
        }

        [HttpGet("{sku}")]
        public IActionResult Details(string sku)
        {
            var product = _catalog.FindBySku(sku.Trim().ToUpperInvariant());
            if (product == null)
            {
                ViewData["Missing"] = sku;
                return View("NotFound");
            }
            return View(product);
        }
    }
}
