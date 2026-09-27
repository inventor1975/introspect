using System.Data.SqlClient;
using Microsoft.AspNetCore.Mvc;

public class HistoryController : Controller
{
    public IActionResult Orders(string customer)
    {
        using (var cmd = new SqlCommand("SELECT * FROM orders WHERE customer = '" + customer + "'"))
        {
            cmd.ExecuteReader();
        }
        return Ok();
    }
}
