package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/dashboard")
public class SavedFilterServlet extends HttpServlet {

    private static final String REGION_KEY = "dashboard.region";

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String region = req.getParameter("region");
        if (region != null && !region.isBlank()) {
            req.getSession().setAttribute(REGION_KEY, region.trim());
        }
        resp.sendRedirect(req.getContextPath() + "/dashboard");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String region = (String) req.getSession().getAttribute(REGION_KEY);
        if (region == null) {
            region = "ALL";
        }
        String sql = "ALL".equals(region)
                ? "SELECT coalesce(sum(amount), 0) FROM sales WHERE sold_on >= date_trunc('month', now())"
                : "SELECT coalesce(sum(amount), 0) FROM sales WHERE sold_on >= date_trunc('month', now()) AND region = '" + region + "'";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            resp.setContentType("text/plain");
            resp.getWriter().println(rs.getBigDecimal(1));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
