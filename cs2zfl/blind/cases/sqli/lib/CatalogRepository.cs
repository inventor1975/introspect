using System.Collections.Generic;
using System.Linq;
using Dapper;
using Microsoft.Data.SqlClient;

namespace Storefront.Data
{
    public class CatalogRepository
    {
        private readonly DbConnections _db;

        public CatalogRepository(DbConnections db)
        {
            _db = db;
        }

        public List<Product> SearchByName(string term)
        {
            using var conn = _db.OpenMain();
            var sql = "SELECT Id, Sku, Name, Category, Price, IsActive FROM Products WHERE Name LIKE '%" + term + "%'";
            return conn.Query<Product>(sql).ToList();
        }

        public Product? FindBySku(string sku)
        {
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Id, Sku, Name, Category, Price, IsActive FROM Products WHERE Sku = @sku", conn);
            cmd.Parameters.AddWithValue("@sku", sku);
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return null;
            }
            return new Product
            {
                Id = reader.GetInt32(0),
                Sku = reader.GetString(1),
                Name = reader.GetString(2),
                Category = reader.GetString(3),
                Price = reader.GetDecimal(4),
                IsActive = reader.GetBoolean(5)
            };
        }
    }
}
