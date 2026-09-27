package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/posts/filter")
public class TagListServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String[] tags = request.getParameterValues("tag");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h3>Filtering by</h3><ul class=\"tags\">");
        if (tags != null) {
            for (String tag : tags) {
                out.print("<li>#");
                out.print(tag);
                out.println("</li>");
            }
        }
        out.println("</ul></body></html>");
    }
}
