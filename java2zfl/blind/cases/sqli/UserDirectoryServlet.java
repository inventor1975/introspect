package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/directory")
public class UserDirectoryServlet extends HttpServlet {

    private static final String BASE = "SELECT display_name, email, phone FROM staff";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String department = request.getParameter("dept");
        String sql = BASE + whereClause(department) + " ORDER BY display_name";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getString("display_name") + " <" + rs.getString("email") + ">");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private String whereClause(String department) {
        if (department == null || department.isBlank()) {
            return " WHERE active = TRUE";
        }
        return " WHERE active = TRUE AND department = '" + department.strip() + "'";
    }
}
