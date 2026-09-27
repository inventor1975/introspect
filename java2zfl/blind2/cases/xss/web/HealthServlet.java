package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/health")
public class HealthServlet extends HttpServlet {

    private static final boolean VERBOSE = false;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String probe = request.getParameter("probe");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h3>Service health</h3><ul>");
        out.println("<li>database: up</li><li>cache: up</li>");
        if (VERBOSE) {
            out.println("<li>probe: " + probe + "</li>");
        }
        out.println("</ul></body></html>");
    }
}
