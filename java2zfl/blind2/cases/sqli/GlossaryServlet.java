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
import org.apache.commons.lang3.StringUtils;

@WebServlet("/glossary")
public class GlossaryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String term = req.getParameter("term");
        if (StringUtils.isBlank(term)) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "term required");
            return;
        }
        if (term.length() > 200) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "term too long");
            return;
        }
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id FROM glossary WHERE lower(term) = lower('" + term.trim() + "')")) {
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.next() ? rs.getLong(1) : -1L);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
