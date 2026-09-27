using System;
using System.Web.UI;

namespace Storefront.Legacy
{
    public partial class TrackShipment : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            var tracking = Request.QueryString["tracking"];
            if (!IsPostBack)
            {
                Response.Write("<h2>Tracking " + Server.HtmlEncode(tracking) + "</h2>");
                Response.Write("<p>Carrier updates may take up to an hour.</p>");
            }
        }
    }
}
