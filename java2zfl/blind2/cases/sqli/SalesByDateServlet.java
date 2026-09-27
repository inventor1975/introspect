package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/sales-by-day")
public class SalesByDateServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        LocalDate from;
        LocalDate to;
        try {
            from = LocalDate.parse(req.getParameter("from"));
            to = LocalDate.parse(req.getParameter("to"));
        } catch (DateTimeParseException | NullPointerException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "from/to must be ISO dates");
            return;
        }
        String sql = "SELECT sold_on, sum(amount) FROM sales WHERE sold_on BETWEEN DATE '" + from + "' AND DATE '" + to
                + "' GROUP BY sold_on ORDER BY sold_on";

        resp.setContentType("text/csv");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getDate(1) + "," + rs.getBigDecimal(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
