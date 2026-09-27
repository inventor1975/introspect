using System.Data.SqlClient;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;

public class ExportController : Controller
{
    private static readonly Regex Identifier = new Regex("^[A-Za-z_][A-Za-z0-9_]*$");

    public IActionResult Table(string table, string other)
    {
        if (!Identifier.IsMatch(table)) return BadRequest();
        new SqlDataAdapter("SELECT * FROM " + table, "cs");
        if (!Regex.IsMatch(other, "[a-z]+")) return BadRequest();   // unanchored: not a guard
        new SqlDataAdapter("SELECT * FROM " + other, "cs");
        return Ok();
    }
}
