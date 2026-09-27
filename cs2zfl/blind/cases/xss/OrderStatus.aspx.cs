using System;
using System.Web.UI;

namespace Storefront.Legacy
{
    public partial class OrderStatus : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            var orderRef = Request.QueryString["order"];
            if (!IsPostBack)
            {
                Response.Write("<h2>Status for order " + orderRef + "</h2>");
                Response.Write("<p>We will email you when it ships.</p>");
            }
        }
    }
}
