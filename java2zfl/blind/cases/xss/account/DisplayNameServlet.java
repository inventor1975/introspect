package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/account/display-name")
public class DisplayNameServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String first = req.getParameter("first");
        String last = req.getParameter("last");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"preview\">This is how others will see you:</div>");
        out.println("<span class=\"display-name\">" + displayName(first, last) + "</span>");
    }

    private static String displayName(String first, String last) {
        StringBuilder full = new StringBuilder();
        if (first != null && !first.isBlank()) {
            full.append(first.trim());
        }
        if (last != null && !last.isBlank()) {
            if (full.length() > 0) {
                full.append(' ');
            }
            full.append(last.trim().charAt(0)).append('.');
        }
        return Encode.forHtml(full.toString());
    }
}
