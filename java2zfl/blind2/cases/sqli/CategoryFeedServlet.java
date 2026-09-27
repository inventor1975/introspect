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

@WebServlet("/feed")
public class CategoryFeedServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String category = req.getParameter("category");
        category = canonical(category);
        String sql = "SELECT id, published_at FROM articles WHERE category = '" + category
                + "' AND published = true ORDER BY published_at DESC LIMIT 20";

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

    private static String canonical(String raw) {
        if (raw == null) {
            return "news";
        }
        switch (raw.trim().toLowerCase(Locale.ROOT)) {
            case "sport":
            case "sports":
                return "sports";
            case "tech":
            case "technology":
                return "technology";
            case "biz":
            case "business":
                return "business";
            default:
                return "news";
        }
    }
}
