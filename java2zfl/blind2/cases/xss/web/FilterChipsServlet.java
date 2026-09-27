package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Arrays;
import java.util.stream.Collectors;
import org.owasp.encoder.Encode;

@WebServlet("/products/filter")
public class FilterChipsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String[] brands = request.getParameterValues("brand");
        String chips = brands == null ? "" : Arrays.stream(brands)
                .filter(b -> !b.isBlank())
                .map(String::trim)
                .map(Encode::forHtml)
                .map(b -> "<span class=\"chip\">" + b + "</span>")
                .collect(Collectors.joining(" "));
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><div class=\"chips\">" + chips + "</div></body></html>");
    }
}
