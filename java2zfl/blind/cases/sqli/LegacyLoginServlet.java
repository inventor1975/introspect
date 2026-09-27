package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/legacy/login")
public class LegacyLoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String user = request.getParameter("username");
        String pass = request.getParameter("password");
        if (StringUtils.isBlank(user) || StringUtils.isBlank(pass)) {
            response.sendRedirect("/legacy/login?error=missing");
            return;
        }
        String query = "SELECT id, role FROM portal_users WHERE username = '" + user
                + "' AND password_hash = MD5('" + pass + "')";
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(query)) {
            if (rs.next()) {
                request.getSession().setAttribute("uid", rs.getLong("id"));
                request.getSession().setAttribute("role", rs.getString("role"));
                response.sendRedirect("/legacy/home");
            } else {
                response.sendRedirect("/legacy/login?error=invalid");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
