package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/albums/rename")
public class RichTitleServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String title = request.getParameter("title");
        String stored = StringEscapeUtils.escapeHtml4(title == null ? "" : title);
        // titles may legitimately contain entities such as &eacute; typed by users
        String display = StringEscapeUtils.unescapeHtml4(stored);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2 class=\"album\">" + display + "</h2><p>Album renamed.</p></body></html>");
    }
}
