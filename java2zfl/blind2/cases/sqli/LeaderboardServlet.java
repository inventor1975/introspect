package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/games/leaderboard")
public class LeaderboardServlet extends HttpServlet {

    private static final Pattern COLUMN = Pattern.compile("^[a-z_]+");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String metric = req.getParameter("metric");
        if (metric == null || !COLUMN.matcher(metric).find()) {
            metric = "total_score";
        }
        String sql = "SELECT player_id, " + metric + " FROM player_stats ORDER BY " + metric + " DESC LIMIT 10";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            int rank = 1;
            while (rs.next()) {
                out.println(rank++ + ". player " + rs.getLong(1) + " - " + rs.getLong(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
