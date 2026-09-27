package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/documents")
public class DocumentAccessServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        String role = (String) session.getAttribute("role");
        String owner = req.getParameter("owner");
        if (owner == null) {
            owner = req.getRemoteUser();
        }

        String scope;
        if ("ADMIN".equals(role)) {
            scope = "1=1";
        } else {
            scope = "owner_login = '" + owner + "'";
        }

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id, size_bytes FROM documents WHERE " + scope + " AND deleted = false")) {
            while (rs.next()) {
                out.println(rs.getLong(1) + " " + rs.getLong(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
