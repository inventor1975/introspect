package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Properties;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/template")
public class ReportTemplateServlet extends HttpServlet {

    private static final Path QUERIES = Path.of("/etc/shop/report-queries.properties");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Properties queries = new Properties();
        try (InputStream in = Files.newInputStream(QUERIES)) {
            queries.load(in);
        }
        String base = queries.getProperty("monthly.revenue", "SELECT month, revenue FROM monthly_revenue");
        String sql = base + " WHERE store_code = ? ORDER BY month";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, request.getParameter("store"));
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getString(1) + " " + rs.getBigDecimal(2));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
