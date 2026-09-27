package blind.sqli;

import blind.sqli.support.Db;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/export")
public class ReportExportServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        StringBuilder body = new StringBuilder();
        try (BufferedReader reader = request.getReader()) {
            String line;
            while ((line = reader.readLine()) != null) {
                body.append(line.trim());
            }
        }
        String filter = body.toString();
        String sql = "SELECT region, product, units, revenue FROM sales_summary";
        if (!filter.isEmpty()) {
            sql = sql + " WHERE " + filter;
        }
        response.setContentType("text/csv");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            if (st.execute(sql)) {
                ResultSet rs = st.getResultSet();
                while (rs.next()) {
                    out.println(rs.getString(1) + "," + rs.getString(2) + "," + rs.getInt(3) + "," + rs.getBigDecimal(4));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
