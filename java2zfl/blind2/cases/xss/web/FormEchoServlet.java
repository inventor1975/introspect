package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;
import java.util.TreeMap;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/forms/review")
public class FormEchoServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Map<String, String[]> fields = new TreeMap<>(request.getParameterMap());
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Please review your answers</h2><table>");
        for (Map.Entry<String, String[]> field : fields.entrySet()) {
            String value = String.join(", ", field.getValue());
            out.println("<tr><th>" + field.getKey() + "</th><td>" + StringEscapeUtils.escapeHtml4(value) + "</td></tr>");
        }
        out.println("</table><button>Submit</button></body></html>");
    }
}
