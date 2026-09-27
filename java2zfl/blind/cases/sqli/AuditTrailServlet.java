package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.UUID;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/audit/note")
public class AuditTrailServlet extends HttpServlet {

    private static final String AUDIT_TABLE = "audit_notes";

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String note = request.getParameter("note");
        String actor = request.getRemoteUser();
        String entryId = UUID.randomUUID().toString();
        String sql = "INSERT INTO " + AUDIT_TABLE + " (entry_id, actor, note, created_at) VALUES ('"
                + entryId + "', ?, ?, CURRENT_TIMESTAMP)";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, actor);
            ps.setString(2, note);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        response.getWriter().println(entryId);
    }
}
