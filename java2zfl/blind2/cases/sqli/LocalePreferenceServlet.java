package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/i18n/messages")
public class LocalePreferenceServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String lang = "en";
        Cookie[] cookies = req.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("lang".equals(c.getName()) && c.getValue() != null) {
                    lang = c.getValue();
                }
            }
        }
        String sql = String.format("SELECT msg_key, msg_text FROM ui_messages WHERE locale = '%s' AND bundle = 'web'", lang);

        Properties bundle = new Properties();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                bundle.setProperty(rs.getString(1), rs.getString(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain;charset=UTF-8");
        bundle.store(resp.getWriter(), null);
    }
}
