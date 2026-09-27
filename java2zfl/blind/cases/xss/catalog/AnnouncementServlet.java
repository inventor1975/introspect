package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/announcement")
public class AnnouncementServlet extends HttpServlet {

    private static volatile String banner = "Free shipping on orders over $50";

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String message = req.getParameter("message");
        if (message != null && !message.isBlank()) {
            banner = message;
        }
        resp.setStatus(HttpServletResponse.SC_OK);
        resp.getWriter().println("updated");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"announcement\">" + banner + "</div>");
    }
}
