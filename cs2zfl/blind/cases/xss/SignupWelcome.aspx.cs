using System;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Storefront.Legacy
{
    public partial class SignupWelcome : Page
    {
        protected Literal litWelcome;

        protected void Page_Load(object sender, EventArgs e)
        {
            litWelcome.Mode = LiteralMode.Encode;
            litWelcome.Text = "Welcome aboard, " + Request.Params["firstName"] + "!";
        }
    }
}
