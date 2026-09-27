using System;
using Microsoft.EntityFrameworkCore;

namespace Storefront.Data
{
    public class Product
    {
        public int Id { get; set; }
        public string Sku { get; set; } = "";
        public string Name { get; set; } = "";
        public string Category { get; set; } = "";
        public decimal Price { get; set; }
        public bool IsActive { get; set; }
    }

    public class Customer
    {
        public int Id { get; set; }
        public string Name { get; set; } = "";
        public string Email { get; set; } = "";
        public string City { get; set; } = "";
    }

    public class Order
    {
        public int Id { get; set; }
        public int CustomerId { get; set; }
        public DateTime PlacedAt { get; set; }
        public string Status { get; set; } = "";
        public decimal Total { get; set; }
    }

    public enum SalesRegion
    {
        North,
        South,
        East,
        West
    }

    public enum SortDirection
    {
        Asc,
        Desc
    }

    public class StoreContext : DbContext
    {
        public StoreContext(DbContextOptions<StoreContext> options) : base(options) { }

        public DbSet<Product> Products => Set<Product>();
        public DbSet<Customer> Customers => Set<Customer>();
        public DbSet<Order> Orders => Set<Order>();
    }
}
