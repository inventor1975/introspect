package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/theme")
public class ThemeServlet extends HttpServlet {

    private static final List<String> THEMES = List.of("light", "dark", "high-contrast");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String theme = req.getParameter("theme");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        if (theme != null && THEMES.contains(theme)) {
            out.println("<link rel=\"stylesheet\" href=\"/css/theme-" + theme + ".css\">");
            out.println("<p>Theme switched to " + theme + ".</p>");
        } else {
            out.println("<p class=\"error\">Unknown theme: " + theme + ". Choose one of " + String.join(", ", THEMES) + ".</p>");
        }
    }
}
