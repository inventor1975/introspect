using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using Npgsql;

namespace Storefront.Data
{
    public class DbConnections
    {
        private readonly string _sqlServer;
        private readonly string _postgres;

        public DbConnections(IConfiguration configuration)
        {
            _sqlServer = configuration.GetConnectionString("Main") ?? "";
            _postgres = configuration.GetConnectionString("Analytics") ?? "";
        }

        public SqlConnection OpenMain()
        {
            var conn = new SqlConnection(_sqlServer);
            conn.Open();
            return conn;
        }

        public NpgsqlConnection OpenAnalytics()
        {
            var conn = new NpgsqlConnection(_postgres);
            conn.Open();
            return conn;
        }
    }
}
