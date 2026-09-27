package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/rooms/bookings")
public class RoomBookingServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String roomId = req.getParameter("room");
        if (roomId != null && roomId.matches("\\d{1,6}")) {
            resp.setContentType("text/plain");
            PrintWriter out = resp.getWriter();
            try (Connection conn = Db.open();
                 Statement st = conn.createStatement();
                 ResultSet rs = st.executeQuery("SELECT slot_start, slot_end FROM room_bookings WHERE room_id = " + roomId
                         + " AND slot_start >= now() ORDER BY slot_start")) {
                while (rs.next()) {
                    out.println(rs.getTimestamp(1) + " - " + rs.getTimestamp(2));
                }
            } catch (SQLException e) {
                throw new ServletException(e);
            }
        } else {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "room must be numeric");
        }
    }
}
