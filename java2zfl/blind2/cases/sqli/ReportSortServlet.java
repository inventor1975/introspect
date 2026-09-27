package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/transactions")
public class ReportSortServlet extends HttpServlet {

    private static final List<String> SORTABLE = List.of("created_at", "amount", "customer_name");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sort = req.getParameter("sort");
        if (sort == null || SORTABLE.stream().noneMatch(sort::startsWith)) {
            sort = "created_at";
        }
        String sql = "SELECT id, amount FROM transactions WHERE booked = true ORDER BY " + sort + " LIMIT 500";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "\t" + rs.getBigDecimal(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
