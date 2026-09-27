package blind2.sqli;

import blind2.sqli.data.CustomerRecord;
import blind2.sqli.data.CustomerRepository;
import blind2.sqli.data.JdbcCustomerRepository;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Optional;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/support/customer")
public class CustomerProfileServlet extends HttpServlet {

    private CustomerRepository customers;

    @Override
    public void init() throws ServletException {
        customers = new JdbcCustomerRepository(DataSources.lookup("jdbc/crm"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String email = req.getParameter("email");
        if (email == null || !email.contains("@")) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "email required");
            return;
        }
        Optional<CustomerRecord> customer;
        try {
            customer = customers.findByEmail(email.trim());
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        if (customer.isEmpty()) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        resp.setContentType("application/json");
        resp.getWriter().print("{\"id\":" + customer.get().id() + "}");
    }
}
