package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/archive-orders")
public class ArchiveMaintenanceServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int olderThanDays;
        try {
            olderThanDays = Integer.parseInt(req.getParameter("olderThanDays"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        if (olderThanDays < 30) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "minimum retention is 30 days");
            return;
        }
        String archiveSchema = System.getenv().getOrDefault("ARCHIVE_SCHEMA", "archive");
        String cutoff = "closed_at < now() - interval '" + olderThanDays + " days'";

        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            conn.setAutoCommit(false);
            int copied = st.executeUpdate("INSERT INTO " + archiveSchema + ".orders SELECT * FROM orders WHERE " + cutoff);
            st.executeUpdate("DELETE FROM orders WHERE " + cutoff);
            conn.commit();
            resp.setContentType("text/plain");
            resp.getWriter().println(copied + " orders archived");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
