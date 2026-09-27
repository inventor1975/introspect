package blind2.sqli;

import blind2.sqli.support.Db;
import blind2.sqli.support.SqlFragments;
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

@WebServlet("/hr/headcount")
public class HeadcountServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String dept = req.getParameter("dept");
        long departmentId;
        try {
            departmentId = Long.parseLong(dept);
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String where = SqlFragments.and(SqlFragments.eq("department_id", departmentId), "terminated_on IS NULL");
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT count(*) FROM employees WHERE " + where)) {
            rs.next();
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.getInt(1));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
