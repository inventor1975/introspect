package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/support/reply/preview")
public class ReplyPreviewServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String reply = req.getParameter("reply");
        if (reply == null) {
            reply = "";
        }
        String escaped = StringEscapeUtils.escapeJava(reply);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h3>Preview</h3>");
        out.println("<div class=\"preview\">" + escaped + "</div>");
    }
}
