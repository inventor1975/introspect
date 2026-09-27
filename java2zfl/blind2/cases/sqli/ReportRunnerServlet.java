package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/run")
public class ReportRunnerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int reportId;
        try {
            reportId = Integer.parseInt(req.getParameter("id"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open()) {
            String view;
            String orderColumn;
            try (PreparedStatement ps = conn.prepareStatement(
                    "SELECT source_view, order_column FROM report_definitions WHERE id = ? AND enabled = true")) {
                ps.setInt(1, reportId);
                try (ResultSet rs = ps.executeQuery()) {
                    if (!rs.next()) {
                        resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                        return;
                    }
                    view = rs.getString(1);
                    orderColumn = rs.getString(2);
                }
            }
            try (Statement st = conn.createStatement();
                 ResultSet rs = st.executeQuery("SELECT * FROM " + view + " ORDER BY " + orderColumn + " LIMIT 1000")) {
                ResultSetMetaData meta = rs.getMetaData();
                int rows = 0;
                while (rs.next()) {
                    rows++;
                }
                out.println(meta.getColumnCount() + " columns, " + rows + " rows");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
