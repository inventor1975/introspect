package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Set;

@WebServlet("/start")
public class LanguagePickerServlet extends HttpServlet {

    private static final Set<String> SUPPORTED = Set.of("en", "de", "fr", "es", "pl");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String lang = request.getParameter("lang");
        if (lang == null || !SUPPORTED.contains(lang)) {
            lang = "en";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<!DOCTYPE html><html lang=\"" + lang + "\"><head>");
        out.println("<script src=\"/static/i18n/" + lang + ".js\"></script></head>");
        out.println("<body data-lang='" + lang + "'><div id=\"app\"></div></body></html>");
    }
}
