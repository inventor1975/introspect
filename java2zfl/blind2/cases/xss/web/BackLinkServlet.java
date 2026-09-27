package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/password-changed")
public class BackLinkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String next = request.getParameter("next");
        if (next == null || !next.startsWith("/") || next.startsWith("//") || next.contains("\\")) {
            next = "/account";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><p>Your password was updated.</p>");
        out.println("<a class=\"btn\" href=\"" + Encode.forHtmlAttribute(next) + "\">Back</a>");
        out.println("</body></html>");
    }
}
