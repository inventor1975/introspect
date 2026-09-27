package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/editor/preview")
public class PreviewPaneServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String draft = request.getParameter("draft");
        String safeDraft = StringEscapeUtils.escapeEcmaScript(draft == null ? "" : draft);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><div class=\"preview\">");
        out.println(safeDraft);
        out.println("</div></body></html>");
    }
}
