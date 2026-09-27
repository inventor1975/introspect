package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/finance/expenses")
public class ExpenseSummaryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String region = request.getParameter("region");
        String yearParam = request.getParameter("year");
        int year;
        try {
            year = Integer.parseInt(yearParam);
        } catch (NumberFormatException e) {
            year = java.time.Year.now().getValue();
        }
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect()) {
            if (region == null) {
                try (Statement st = conn.createStatement();
                     ResultSet rs = st.executeQuery(ReportSqlBuilder.forYear(year))) {
                    print(rs, out);
                }
            } else {
                try (PreparedStatement ps = conn.prepareStatement(ReportSqlBuilder.forRegionParam())) {
                    ps.setString(1, region);
                    ps.setInt(2, year);
                    try (ResultSet rs = ps.executeQuery()) {
                        print(rs, out);
                    }
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private static void print(ResultSet rs, PrintWriter out) throws SQLException {
        while (rs.next()) {
            out.println(rs.getString("department") + ": " + rs.getBigDecimal("total"));
        }
    }
}
