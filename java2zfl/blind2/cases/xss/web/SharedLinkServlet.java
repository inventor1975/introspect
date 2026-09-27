package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@WebServlet("/s")
public class SharedLinkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String token = request.getParameter("t");
        String title;
        try {
            byte[] decoded = Base64.getUrlDecoder().decode(token);
            title = new String(decoded, StandardCharsets.UTF_8);
        } catch (IllegalArgumentException | NullPointerException e) {
            title = "Shared item";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><head><title>Shared with you</title></head><body>");
        out.println("<h2>" + title + "</h2><p>Someone shared this item with you.</p>");
        out.println("</body></html>");
    }
}
