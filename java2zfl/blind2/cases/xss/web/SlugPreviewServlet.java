package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.regex.Pattern;

@WebServlet("/cms/slug")
public class SlugPreviewServlet extends HttpServlet {

    private static final Pattern SLUG = Pattern.compile("[a-z0-9-]+");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String slug = request.getParameter("slug");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        if (slug == null || !SLUG.matcher(slug).find()) {
            out.println("<p class=\"err\">Slugs may only contain lowercase letters, digits and dashes.</p>");
            return;
        }
        out.println("<p>Your page will be published at <a href=\"/p/" + slug + "\">/p/" + slug + "</a></p>");
    }
}
