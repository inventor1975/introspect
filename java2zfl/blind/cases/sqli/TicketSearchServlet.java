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

@WebServlet("/helpdesk/tickets")
public class TicketSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String field = request.getParameter("field");
        String value = request.getParameter("value");
        String column;
        switch (field == null ? "" : field) {
            case "assignee":
                column = "assignee_login";
                break;
            case "reporter":
                column = "reporter_login";
                break;
            case "status":
                column = "status_code";
                break;
            default:
                column = "subject";
        }
        String sql = "SELECT id, subject, status_code FROM tickets WHERE " + column + " = '" + value + "'";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println("#" + rs.getInt("id") + " " + rs.getString("subject"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
