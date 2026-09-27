using Microsoft.AspNetCore.Mvc;

public class StatementController : Controller
{
    [HttpGet("{year:int}/{id}")]
    public IActionResult Pdf(int year, string id)
    {
        System.IO.File.ReadAllBytes("/srv/statements/" + year + ".pdf");   // an int carries no text
        return PhysicalFile("/srv/statements/" + id + ".pdf", "application/pdf");
    }
}
