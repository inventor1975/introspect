package blind.xss.account;

import blind.xss.common.Markup;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/welcome")
public class WelcomeBackServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String name = req.getParameter("name");
        if (name == null) {
            name = "friend";
        }
        String body = Markup.tag("h2", "Welcome back")
                + Markup.tag("p", "Hello again, " + name + ". You have new messages.")
                + Markup.link("/account/messages", "Open inbox");
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter().print(Markup.page("Welcome back", body));
    }
}
