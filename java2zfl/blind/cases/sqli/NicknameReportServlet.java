package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/community/activity")
public class NicknameReportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        long memberId;
        try {
            memberId = Long.parseLong(request.getParameter("member"));
        } catch (NumberFormatException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect()) {
            String nickname = null;
            try (PreparedStatement ps = conn.prepareStatement("SELECT nickname FROM members WHERE id = ?")) {
                ps.setLong(1, memberId);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        nickname = rs.getString(1);
                    }
                }
            }
            if (nickname == null) {
                response.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            try (Statement st = conn.createStatement();
                 ResultSet posts = st.executeQuery("SELECT title, posted_at FROM forum_posts WHERE author_nick = '"
                         + nickname + "' ORDER BY posted_at DESC LIMIT 20")) {
                while (posts.next()) {
                    out.println(posts.getString("title"));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
