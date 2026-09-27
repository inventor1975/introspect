package blind2.sqli;

import blind2.sqli.support.AbstractListServlet;
import java.io.IOException;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/helpdesk/tickets/open-count")
public class TicketListServlet extends AbstractListServlet {

    @Override
    protected String table() {
        return "support_tickets";
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String assignee = req.getParameter("assignee");
        String condition = assignee == null
                ? "state = 'OPEN'"
                : "state = 'OPEN' AND assignee_login = '" + assignee + "'";
        int open;
        try {
            open = countWhere(condition);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().print(open);
    }
}
