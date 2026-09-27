package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.regex.Pattern;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/reset")
public class PasswordResetServlet extends HttpServlet {

    private static final Pattern TOKEN = Pattern.compile("[A-Za-z0-9]{32}");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String token = req.getParameter("token");
        if (token == null || !TOKEN.matcher(token).matches()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "This reset link is invalid or has expired.");
            return;
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<form method=\"post\" action=\"/account/reset\">");
        out.println("  <input type=\"hidden\" name=\"token\" value=\"" + token + "\">");
        out.println("  <label>New password <input type=\"password\" name=\"password\"></label>");
        out.println("  <button type=\"submit\">Reset password</button>");
        out.println("</form>");
        out.println("<p class=\"hint\">Reference: " + token.substring(0, 6) + "&hellip;</p>");
    }
}
