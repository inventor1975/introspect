package blind.xss.catalog;

import blind.xss.common.Markup;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/category")
public class CategoryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String category = req.getParameter("name");
        String next = req.getParameter("next");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println(Markup.tag("h2", Markup.text(category)));
        out.println("<div id=\"products\"></div>");
        if (next != null) {
            out.println(Markup.link(next, "More in " + category));
        }
    }
}
