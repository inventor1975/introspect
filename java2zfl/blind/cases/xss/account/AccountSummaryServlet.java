package blind.xss.account;

import blind.xss.common.Markup;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/summary")
public class AccountSummaryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String name = req.getParameter("name");
        if (name == null) {
            name = "Customer";
        }
        String body = Markup.tag("h2", "Account for " + Markup.text(name))
                + Markup.tag("p", "Signed in as " + Markup.text(name))
                + Markup.link("/account/orders", "Orders for " + name);
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter().print(Markup.page("Account for " + name, body));
    }
}
