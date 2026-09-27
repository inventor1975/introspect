package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/home")
public class AnnouncementServlet extends HttpServlet {

    private String bannerHtml;

    @Override
    public void init() throws ServletException {
        bannerHtml = getInitParameter("announcementHtml");
        if (bannerHtml == null) {
            bannerHtml = "";
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String section = request.getParameter("section");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<div class=\"announcement\">" + bannerHtml + "</div>");
        out.println("<div id=\"content\" data-section-length=\"" + (section == null ? 0 : section.length()) + "\"></div>");
        out.println("</body></html>");
    }
}
