package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/drafts/archive")
public class BulkArchiveServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String[] raw = request.getParameterValues("id");
        if (raw == null || raw.length == 0) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        List<Long> ids = new ArrayList<>();
        for (String r : raw) {
            try {
                ids.add(Long.parseLong(r.trim()));
            } catch (NumberFormatException e) {
                response.sendError(HttpServletResponse.SC_BAD_REQUEST, "bad id");
                return;
            }
        }
        String idList = ids.stream().map(String::valueOf).collect(Collectors.joining(","));
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            int n = st.executeUpdate("UPDATE drafts SET archived = TRUE WHERE id IN (" + idList + ")");
            response.getWriter().println(n + " drafts archived");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
