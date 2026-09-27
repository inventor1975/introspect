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
import javax.servlet.http.HttpSession;

@WebServlet("/region/dashboard")
public class RegionDashboardServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        Object selected = session == null ? null : session.getAttribute("selectedRegion");
        String region = selected == null ? "GLOBAL" : selected.toString();
        String sql = "SELECT store_code, revenue_today, open_orders FROM store_kpis WHERE region = '"
                + region + "' ORDER BY revenue_today DESC";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getString("store_code") + " " + rs.getBigDecimal("revenue_today"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
