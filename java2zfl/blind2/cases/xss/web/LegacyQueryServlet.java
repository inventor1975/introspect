package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

@WebServlet("/legacy/search.do")
public class LegacyQueryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String qs = request.getQueryString();
        String criteria = qs == null ? "" : URLDecoder.decode(qs, StandardCharsets.UTF_8);
        response.setContentType("text/html;charset=ISO-8859-1");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<p>This page has moved. Your search criteria were: <code>" + criteria + "</code></p>");
        out.println("<a href=\"/search\">Go to the new search</a></body></html>");
    }
}
