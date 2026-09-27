using System;
using System.IO;
using System.Web.UI;

namespace LegacyIntranet
{
    public partial class DocumentViewer : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            var doc = Request.QueryString["doc"];
            if (string.IsNullOrEmpty(doc))
            {
                Response.Redirect("~/Documents.aspx");
                return;
            }

            var docsRoot = Server.MapPath("~/App_Data/documents");
            var path = Path.Combine(docsRoot, doc);

            Response.Clear();
            Response.ContentType = "application/octet-stream";
            Response.AddHeader("Content-Disposition", "attachment; filename=" + Path.GetFileName(path));
            Response.WriteFile(path);
            Response.End();
        }
    }
}
