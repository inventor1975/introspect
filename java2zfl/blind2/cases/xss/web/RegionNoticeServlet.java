package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/region")
public class RegionNoticeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String region = request.getParameter("region");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        if (region != null && (region.startsWith("eu-") || region.startsWith("us-"))) {
            out.println("<p>Serving you from data centre <b>" + region + "</b>.</p>");
        } else {
            out.println("<p>Serving you from the nearest data centre.</p>");
        }
        out.println("</body></html>");
    }
}
