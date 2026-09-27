using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Storefront.Legacy
{
    public partial class OrderHistory : Page
    {
        protected GridView OrdersGrid;

        protected void Page_Load(object sender, EventArgs e)
        {
            if (IsPostBack)
            {
                return;
            }

            string customer = Request.QueryString["customer"];
            string from = Request.QueryString["from"] ?? "2000-01-01";
            string sql = "SELECT Id, PlacedAt, Status, Total FROM Orders WHERE CustomerId = " + customer
                         + " AND PlacedAt >= '" + from + "' ORDER BY PlacedAt DESC";

            using (var conn = new SqlConnection(ConfigurationManager.ConnectionStrings["Main"].ConnectionString))
            using (var cmd = new SqlCommand(sql, conn))
            using (var adapter = new SqlDataAdapter(cmd))
            {
                var table = new DataTable();
                adapter.Fill(table);
                OrdersGrid.DataSource = table;
                OrdersGrid.DataBind();
            }
        }
    }
}
