package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/help/faq")
public class FaqSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String topic = "general";
        String query = req.getQueryString();
        if (query != null) {
            for (String pair : query.split("&")) {
                int eq = pair.indexOf('=');
                if (eq > 0 && "topic".equals(pair.substring(0, eq))) {
                    topic = URLDecoder.decode(pair.substring(eq + 1), StandardCharsets.UTF_8);
                }
            }
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id FROM faq_entries WHERE topic = '" + topic + "' ORDER BY position")) {
            while (rs.next()) {
                out.println(rs.getInt(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
