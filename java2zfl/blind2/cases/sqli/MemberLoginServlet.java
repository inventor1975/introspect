package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/members/login")
public class MemberLoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        if (username == null || password == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        Long memberId;
        try {
            memberId = authenticate(username.trim(), sha256(password));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        if (memberId == null) {
            resp.sendRedirect(req.getContextPath() + "/members/login?failed=1");
            return;
        }
        req.getSession().setAttribute("memberId", memberId);
        resp.sendRedirect(req.getContextPath() + "/members/home");
    }

    private Long authenticate(String login, String passwordHash) throws SQLException {
        String sql = "SELECT id FROM members WHERE login = '" + login + "' AND password_hash = '" + passwordHash + "'";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            return rs.next() ? rs.getLong(1) : null;
        }
    }

    private static String sha256(String value) throws ServletException {
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8));
            StringBuilder hex = new StringBuilder();
            for (byte b : digest) {
                hex.append(String.format("%02x", b));
            }
            return hex.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new ServletException(e);
        }
    }
}
