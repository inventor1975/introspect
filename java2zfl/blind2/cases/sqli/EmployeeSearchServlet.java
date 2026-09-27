package blind2.sqli;

import blind2.sqli.support.Db;
import blind2.sqli.support.SqlFragments;
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

@WebServlet("/hr/employees")
public class EmployeeSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        long departmentId;
        try {
            departmentId = Long.parseLong(req.getParameter("dept"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "dept must be numeric");
            return;
        }
        String name = req.getParameter("name");
        String where = name == null
                ? SqlFragments.eq("department_id", departmentId)
                : SqlFragments.and(SqlFragments.eq("department_id", departmentId), SqlFragments.like("last_name", name));

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT employee_no FROM employees WHERE " + where + " ORDER BY last_name")) {
            while (rs.next()) {
                out.println(rs.getInt(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
