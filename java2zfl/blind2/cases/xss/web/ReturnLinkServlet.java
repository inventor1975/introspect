package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/logout-complete")
public class ReturnLinkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String next = request.getParameter("next");
        if (next == null || next.isEmpty()) {
            next = "/";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><p>You have been signed out.</p>");
        out.println("<a class=\"btn\" href=\"" + Encode.forHtmlAttribute(next) + "\">Continue</a>");
        out.println("</body></html>");
    }
}
