package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/metrics/beacon")
public class MetricsServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        int loadMs = request.getIntHeader("X-Page-Load-Ms");
        int status = request.getIntHeader("X-Page-Status");
        String pageKey = request.getHeader("X-Page-Key");
        if (loadMs < 0 || pageKey == null) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        StringBuilder sql = new StringBuilder("INSERT INTO page_timings (bucket, load_ms, http_status, recorded_at) VALUES (");
        sql.append(pageKey.hashCode() & 0xff).append(", ");
        sql.append(loadMs).append(", ");
        sql.append(status).append(", CURRENT_TIMESTAMP)");
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            st.executeUpdate(sql.toString());
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        response.setStatus(HttpServletResponse.SC_OK);
    }
}
