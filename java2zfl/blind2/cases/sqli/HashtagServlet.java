package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Locale;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/social/hashtag")
public class HashtagServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String tag = req.getParameter("tag");
        if (tag != null && tag.startsWith("#")) {
            tag = tag.substring(1);
        }
        if (!isPlainWord(tag)) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "hashtags may only contain letters, digits and underscores");
            return;
        }
        String sql = "SELECT post_id FROM post_hashtags WHERE tag = '" + tag.toLowerCase(Locale.ROOT)
                + "' ORDER BY post_id DESC LIMIT 100";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private static boolean isPlainWord(String s) {
        if (s == null || s.isEmpty() || s.length() > 64) {
            return false;
        }
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            boolean ok = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_';
            if (!ok) {
                return false;
            }
        }
        return true;
    }
}
