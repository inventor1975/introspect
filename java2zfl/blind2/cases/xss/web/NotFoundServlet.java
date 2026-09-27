package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/wiki/page")
public class NotFoundServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String page = request.getParameter("title");
        String safeTitle = Encode.forHtml(page == null ? "" : page);
        response.setStatus(HttpServletResponse.SC_NOT_FOUND);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><head><title>" + safeTitle + " - not found</title></head><body>");
        out.println("<h1>No page called &ldquo;" + page + "&rdquo;</h1>");
        out.println("<a href=\"/wiki/new\">Create it</a></body></html>");
    }
}
