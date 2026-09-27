package blind2.sqli;

import blind2.sqli.data.NewsletterDao;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.sql.SQLException;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/newsletter/subscribe")
public class SubscriberServlet extends HttpServlet {

    private static final Logger LOG = Logger.getLogger(SubscriberServlet.class.getName());

    private NewsletterDao newsletter;

    @Override
    public void init() throws ServletException {
        newsletter = new NewsletterDao(DataSources.lookup("jdbc/marketing"));
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String email = req.getParameter("email");
        String list = req.getParameter("list");
        if (email == null || !email.contains("@")) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "valid email required");
            return;
        }
        if (list == null || list.isBlank()) {
            list = "weekly";
        }
        boolean added;
        try {
            added = newsletter.subscribe(email.trim().toLowerCase(), list);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        LOG.info("newsletter subscribe list=" + list.replaceAll("[\\r\\n]", "") + " added=" + added);
        resp.sendRedirect(req.getContextPath() + "/newsletter/thanks");
    }
}
