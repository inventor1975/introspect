package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/compare")
public class ProductTooltipServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String note = request.getParameter("note");
        String sku = request.getParameter("sku");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><table><tr>");
        out.println("<td class=\"sku\" title=\"" + Encode.forHtmlContent(note == null ? "" : note) + "\">"
                + Encode.forHtmlContent(sku == null ? "" : sku) + "</td>");
        out.println("</tr></table></body></html>");
    }
}
