package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/preferences")
public class PreferencesServlet extends HttpServlet {

    private String accentColour = "teal";

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String requested = req.getParameter("accent");
        if (requested != null && !requested.isBlank()) {
            accentColour = requested.trim();
        }
        resp.sendRedirect("/account/preferences");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h2>Preferences</h2>");
        out.println("<p>Accent colour: <span class=\"swatch\">" + accentColour + "</span></p>");
        out.println("<form method=\"post\"><input name=\"accent\"><button>Change</button></form>");
    }
}
