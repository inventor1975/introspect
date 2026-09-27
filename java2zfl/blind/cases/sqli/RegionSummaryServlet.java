package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/finance/regions")
public class RegionSummaryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String region = request.getParameter("region");
        String table;
        switch (region == null ? "" : region.toUpperCase()) {
            case "EMEA":
                table = "sales_emea";
                break;
            case "APAC":
                table = "sales_apac";
                break;
            case "AMER":
                table = "sales_amer";
                break;
            default:
                response.sendError(HttpServletResponse.SC_BAD_REQUEST, "unknown region");
                return;
        }
        String sql = "SELECT country, SUM(revenue) FROM " + table + " GROUP BY country ORDER BY 2 DESC";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getString(1) + " " + rs.getBigDecimal(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
