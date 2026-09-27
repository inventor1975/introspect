package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/orders")
public class SortOrderServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String dir = request.getParameter("dir");
        if (dir == null || !(dir.equalsIgnoreCase("asc") || dir.equalsIgnoreCase("desc"))) {
            dir = "desc";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<table id=\"orders\" data-sort-dir=\"" + dir + "\"><thead><tr><th>Date (" + dir + ")</th></tr></thead></table>");
        out.println("</body></html>");
    }
}
