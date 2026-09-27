package blind2.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

/** Base class for the dashboard pages: shared chrome around a body fragment. */
public abstract class LayoutServlet extends HttpServlet {

    protected void writePage(HttpServletResponse response, String title, String bodyHtml) throws IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<!DOCTYPE html><html><head><meta charset=\"utf-8\">");
        out.println("<title>" + Encode.forHtml(title) + " | Dashboard</title></head><body>");
        out.println("<nav><a href=\"/dashboard\">Home</a></nav>");
        out.println("<main>");
        out.println(bodyHtml);
        out.println("</main></body></html>");
    }
}
