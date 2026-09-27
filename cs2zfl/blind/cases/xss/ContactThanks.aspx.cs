using System;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Storefront.Legacy
{
    public partial class ContactThanks : Page
    {
        protected Literal litGreeting;

        protected void Page_Load(object sender, EventArgs e)
        {
            string first = Request.Params["firstName"];
            litGreeting.Text = "<p>Thank you, " + first + ". We received your message.</p>";
        }
    }
}
