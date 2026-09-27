package blind2.sqli;

import blind2.sqli.support.Db;
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
import org.owasp.encoder.Encode;

@WebServlet("/reports/members-by-age")
public class MemberAgeReportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String minAge = req.getParameter("minAge");
        if (minAge == null || minAge.isEmpty()) {
            minAge = "18";
        }
        String cleanMin = Encode.forHtml(minAge);
        String sql = "SELECT count(*) FROM members WHERE date_part('year', age(birth_date)) >= " + cleanMin;

        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            resp.setContentType("text/html");
            resp.getWriter().println("<p>Members aged " + cleanMin + "+: " + rs.getInt(1) + "</p>");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
