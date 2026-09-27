using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("catalog")]
    public class CatalogSearchController : Controller
    {
        private readonly CatalogRepository _catalog;

        public CatalogSearchController(CatalogRepository catalog)
        {
            _catalog = catalog;
        }

        [HttpGet("search")]
        public IActionResult Search([FromQuery(Name = "q")] string query)
        {
            if (string.IsNullOrWhiteSpace(query))
            {
                return RedirectToAction("Index", "Home");
            }
            var results = _catalog.SearchByName(query.Trim());
            ViewData["Query"] = query;
            return View(results);
        }
    }
}
