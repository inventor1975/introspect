package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Locale;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/help/articles")
public class ArticleIndexServlet extends HttpServlet {

    private static final String[] TITLES = {
        "Resetting your password",
        "Updating billing details",
        "Exporting your data",
        "Closing your account",
        "Setting up two-factor authentication",
    };
    private static final int PAGE_SIZE = 3;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String filter = req.getParameter("filter");
        int start = 0;
        try {
            start = Math.max(0, Integer.parseInt(req.getParameter("start")));
        } catch (NumberFormatException ignored) {
            // first page
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<ol class=\"articles\" start=\"" + (start + 1) + "\">");
        int shown = 0;
        for (int i = start; i < TITLES.length; i++) {
            if (filter != null && !TITLES[i].toLowerCase(Locale.ROOT).contains(filter.toLowerCase(Locale.ROOT))) {
                continue;
            }
            if (shown == PAGE_SIZE) {
                break;
            }
            out.println("<li><a href=\"/help/articles/" + i + "\">" + TITLES[i] + "</a></li>");
            shown++;
        }
        out.println("</ol>");
        if (shown == 0) {
            out.println("<p>No matching articles.</p>");
        }
    }
}
