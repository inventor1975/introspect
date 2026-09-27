package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Arrays;
import java.util.stream.Collectors;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/fulfilment/mark-printed")
public class OrderIdsServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] raw = req.getParameterValues("id");
        if (raw == null || raw.length == 0) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String ids;
        try {
            ids = Arrays.stream(raw)
                    .map(String::trim)
                    .map(Long::parseLong)
                    .map(String::valueOf)
                    .collect(Collectors.joining(","));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "order ids must be numeric");
            return;
        }
        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            int n = st.executeUpdate("UPDATE orders SET label_printed = true WHERE id IN (" + ids + ")");
            resp.setContentType("text/plain");
            resp.getWriter().println(n);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
