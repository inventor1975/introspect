package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/columns")
public class ColumnPickerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        List<String> columns = Arrays.asList(
                Optional.ofNullable(req.getParameter("cols")).orElse("id,name,created").split(","));
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<table class=\"report\"><thead><tr>");
        columns.stream()
                .map(String::trim)
                .filter(c -> !c.isEmpty())
                .forEach(c -> out.println("<th>" + c + "</th>"));
        out.println("</tr></thead><tbody id=\"rows\"></tbody></table>");
    }
}
