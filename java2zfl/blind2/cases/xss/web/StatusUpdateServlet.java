package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.regex.Pattern;

@WebServlet("/status")
public class StatusUpdateServlet extends HttpServlet {

    private static final Pattern SCRIPT_TAG = Pattern.compile("(?is)<script.*?>.*?</script>");

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String status = request.getParameter("status");
        if (status == null) {
            status = "";
        }
        String cleaned = SCRIPT_TAG.matcher(status).replaceAll("");
        cleaned = cleaned.replaceAll("(?i)javascript:", "");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><div class=\"status\">" + cleaned + "</div>");
        out.println("<small>Posted just now</small></body></html>");
    }
}
