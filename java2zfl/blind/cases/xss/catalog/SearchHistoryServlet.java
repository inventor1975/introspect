package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/search/history")
public class SearchHistoryServlet extends HttpServlet {

    private static final String KEY = "recentSearches";

    @Override
    @SuppressWarnings("unchecked")
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String q = req.getParameter("q");
        HttpSession session = req.getSession();
        List<String> recent = (List<String>) session.getAttribute(KEY);
        if (recent == null) {
            recent = new ArrayList<>();
        }
        if (q != null && !q.isBlank()) {
            recent.add(0, q.trim());
            if (recent.size() > 10) {
                recent.remove(recent.size() - 1);
            }
        }
        session.setAttribute(KEY, recent);
        resp.sendRedirect("/search/history");
    }

    @Override
    @SuppressWarnings("unchecked")
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        List<String> recent = session == null ? List.of() : (List<String>) session.getAttribute(KEY);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h3>Recent searches</h3><ul>");
        if (recent != null) {
            for (String term : recent) {
                out.println("<li>" + term + "</li>");
            }
        }
        out.println("</ul>");
    }
}
