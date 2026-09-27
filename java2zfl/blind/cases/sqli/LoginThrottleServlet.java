package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HexFormat;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/login/precheck")
public class LoginThrottleServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String username = request.getParameter("username");
        if (username == null) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String key = fingerprint(username.toLowerCase());
        String sql = "SELECT failures FROM login_throttle WHERE user_key = '" + key
                + "' AND window_start > NOW() - INTERVAL '15 minutes'";
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            boolean locked = rs.next() && rs.getInt(1) >= 5;
            response.setStatus(locked ? HttpServletResponse.SC_FORBIDDEN : HttpServletResponse.SC_OK);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private static String fingerprint(String value) throws ServletException {
        try {
            MessageDigest sha = MessageDigest.getInstance("SHA-256");
            return HexFormat.of().formatHex(sha.digest(value.getBytes(StandardCharsets.UTF_8)));
        } catch (NoSuchAlgorithmException e) {
            throw new ServletException(e);
        }
    }
}
