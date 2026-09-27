package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/*")
public class CatalogPageServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String path = request.getPathInfo();
        if (path == null || path.equals("/")) {
            path = "/all";
        }
        String[] segments = path.substring(1).split("/");
        StringBuilder crumbs = new StringBuilder("<a href=\"/catalog/\">Catalog</a>");
        for (String seg : segments) {
            crumbs.append(" &raquo; <span>").append(seg).append("</span>");
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><nav class=\"crumbs\">" + crumbs + "</nav>");
        out.println("<div id=\"grid\" data-src=\"/api/catalog\"></div></body></html>");
    }
}
