package blind2.sqli;

import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;

@WebServlet("/ops/orders/by-status")
public class OrderStatusProcServlet extends HttpServlet {

    private DataSource erp;

    @Override
    public void init() throws ServletException {
        erp = DataSources.lookup("jdbc/erp");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String status = req.getParameter("status");
        if (status == null) {
            status = "PENDING";
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = erp.getConnection();
             CallableStatement cs = conn.prepareCall("{call orders_by_status('" + status + "')}");
             ResultSet rs = cs.executeQuery()) {
            while (rs.next()) {
                out.println(rs.getLong("order_id"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
