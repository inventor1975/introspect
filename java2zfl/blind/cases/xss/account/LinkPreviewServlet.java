package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/account/website-preview")
public class LinkPreviewServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String url = req.getParameter("url");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        if (url == null || !(url.startsWith("https://") || url.startsWith("http://"))) {
            out.println("<p class=\"warn\">Only web addresses starting with http:// or https:// can be shown on your profile.</p>");
            return;
        }
        out.println("<p>Your website will appear as:</p>");
        out.println("<a rel=\"nofollow noopener\" target=\"_blank\" href=\"" + Encode.forHtmlAttribute(url) + "\">"
                + Encode.forHtml(url) + "</a>");
    }
}
