package blind.xss.catalog;

import java.io.IOException;
import java.util.Arrays;
import java.util.stream.Collectors;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/catalog/tags")
public class TagListServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] tags = req.getParameterValues("tag");
        String items = tags == null ? "" : Arrays.stream(tags)
                .filter(t -> t != null && !t.isBlank())
                .map(String::trim)
                .distinct()
                .map(Encode::forHtml)
                .map(t -> "<li class=\"tag\">" + t + "</li>")
                .collect(Collectors.joining("\n"));
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter().println("<ul class=\"tags\">" + items + "</ul>");
    }
}
