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

@WebServlet("/articles/*")
public class ArticleSlugServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getPathInfo();
        if (path == null || path.length() < 2) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        String slug = path.substring(1);
        if (slug.endsWith("/")) {
            slug = slug.substring(0, slug.length() - 1);
        }

        String sql = "SELECT id, word_count FROM articles WHERE slug = '" + slug + "' AND published = true";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            if (!rs.next()) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            req.setAttribute("articleId", rs.getLong(1));
            req.setAttribute("wordCount", rs.getInt(2));
            resp.setContentType("text/plain");
            resp.getWriter().println("article " + rs.getLong(1));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
