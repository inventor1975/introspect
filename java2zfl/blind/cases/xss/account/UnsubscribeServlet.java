package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.regex.Pattern;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/unsubscribe")
public class UnsubscribeServlet extends HttpServlet {

    private static final Pattern EMAIL = Pattern.compile("^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,190}\\.[A-Za-z]{2,24}$");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String email = req.getParameter("email");
        if (email == null || !EMAIL.matcher(email).matches()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h2>Unsubscribe</h2>");
        out.println("<p>We will stop sending the newsletter to <b>" + email + "</b>.</p>");
        out.println("<form method=\"post\"><input type=\"hidden\" name=\"email\" value=\"" + email + "\">"
                + "<button>Confirm</button></form>");
    }
}
