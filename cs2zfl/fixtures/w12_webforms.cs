using System;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Welcome : Page
{
    protected Label lblName;
    protected Literal litSafe;
    protected TextBox txtName;

    protected void Page_Load(object sender, EventArgs e)
    {
        lblName.Text = "Hi " + Request.QueryString["name"];      // a Label renders HTML as is
        litSafe.Mode = LiteralMode.Encode;
        litSafe.Text = Request.QueryString["name"];
        txtName.Text = Request.QueryString["name"];               // a TextBox encodes its value
    }
}
