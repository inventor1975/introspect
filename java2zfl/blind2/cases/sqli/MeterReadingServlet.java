package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.regex.Pattern;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/utility/meter-readings")
public class MeterReadingServlet extends HttpServlet {

    private static final Pattern METER_ID = Pattern.compile("^\\d{1,9}$");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String meter = req.getParameter("meter");
        if (meter == null || !METER_ID.matcher(meter).matches()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid meter id");
            return;
        }
        String sql = "SELECT reading_kwh, read_at FROM meter_readings WHERE meter_id = " + meter
                + " ORDER BY read_at DESC LIMIT 12";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getTimestamp(2) + "\t" + rs.getBigDecimal(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
