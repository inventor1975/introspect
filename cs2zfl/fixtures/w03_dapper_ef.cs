using Dapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

public class SearchController : ControllerBase
{
    private readonly System.Data.IDbConnection _conn;
    private readonly ShopContext _db;

    public IActionResult Find(string q)
    {
        var rows = _conn.Query<Item>("SELECT * FROM items WHERE name = '" + q + "'");
        var more = _db.Items.FromSqlRaw("SELECT * FROM items WHERE tag = '" + q + "'").ToList();
        var safe = _db.Items.FromSqlInterpolated($"SELECT * FROM items WHERE tag = {q}").ToList();   // parameterised
        return Ok(rows);
    }
}
