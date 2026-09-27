package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Set;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/language")
public class LocaleBannerServlet extends HttpServlet {

    private static final Set<String> SUPPORTED = Set.of("en", "de", "fr", "es", "pt");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String lang = req.getParameter("lang");
        if (lang == null || !SUPPORTED.contains(lang)) {
            lang = "en";
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<!DOCTYPE html><html lang=\"" + lang + "\"><body>");
        out.println("<div class=\"banner banner-" + lang + "\">");
        out.println("<img src=\"/static/flags/" + lang + ".svg\" alt=\"\"> Language: " + lang);
        out.println("</div></body></html>");
    }
}
