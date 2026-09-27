package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.regex.Pattern;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/tags/related")
public class TagCloudServlet extends HttpServlet {

    private static final Pattern TAG = Pattern.compile("^[a-z0-9_-]{1,32}$");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String tag = request.getParameter("tag");
        if (tag == null || !TAG.matcher(tag).matches()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid tag");
            return;
        }
        String sql = "SELECT t2.name, COUNT(*) FROM post_tags a JOIN post_tags b ON a.post_id = b.post_id"
                + " JOIN tags t1 ON t1.id = a.tag_id JOIN tags t2 ON t2.id = b.tag_id"
                + " WHERE t1.name = '" + tag + "' AND t2.name <> '" + tag + "' GROUP BY t2.name ORDER BY 2 DESC LIMIT 15";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getString(1) + " (" + rs.getInt(2) + ")");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
