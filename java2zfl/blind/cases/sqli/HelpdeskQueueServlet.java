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

@WebServlet("/helpdesk/queue")
public class HelpdeskQueueServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String queue = request.getParameter("queue");
        String sql = queueQuery(queue);
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

    private String queueQuery(String queue) {
        if (queue != null && !queue.isEmpty()) {
            System.out.println("queue view requested: " + queue);
        }
        boolean urgentOnly = "urgent".equalsIgnoreCase(queue);
        return "SELECT id, subject FROM tickets WHERE closed = FALSE"
                + (urgentOnly ? " AND priority >= 4" : "")
                + " ORDER BY opened_at";
    }
}
