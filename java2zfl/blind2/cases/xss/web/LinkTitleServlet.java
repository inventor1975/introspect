package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/bookmarks/add")
public class LinkTitleServlet extends HttpServlet {

    private static String clean(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String label = request.getParameter("label");
        if (label == null || label.isBlank()) {
            label = "Untitled";
        }
        long id = System.currentTimeMillis();
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><p>Bookmark saved.</p>");
        out.println("<a href=\"/bookmarks/" + id + "\" title=\"" + clean(label) + "\">" + clean(label) + "</a>");
        out.println("</body></html>");
    }
}
