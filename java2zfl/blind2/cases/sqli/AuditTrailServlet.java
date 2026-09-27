package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/audit")
public class AuditTrailServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        StringBuilder where = new StringBuilder(" WHERE 1=1");
        for (Map.Entry<String, String[]> e : req.getParameterMap().entrySet()) {
            String name = e.getKey();
            if (name.startsWith("f_") && e.getValue().length > 0 && !e.getValue()[0].isEmpty()) {
                where.append(" AND ").append(name.substring(2)).append(" = '").append(e.getValue()[0]).append("'");
            }
        }
        String sql = "SELECT id, occurred_at FROM audit_events" + where + " ORDER BY occurred_at DESC LIMIT 200";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "\t" + rs.getTimestamp(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
