package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/staff/lookup")
public class StaffLookupServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String by = request.getParameter("by");
        String value = request.getParameter("q");
        String column = "email".equals(by) ? "email" : "username";
        String sql = "SELECT display_name, email, extension FROM staff WHERE " + column + " = ?";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, value);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getString("display_name") + " x" + rs.getString("extension"));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
