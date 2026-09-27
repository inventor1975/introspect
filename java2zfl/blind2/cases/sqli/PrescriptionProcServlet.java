package blind2.sqli;

import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;

@WebServlet("/pharmacy/prescriptions")
public class PrescriptionProcServlet extends HttpServlet {

    private DataSource pharmacy;

    @Override
    public void init() throws ServletException {
        pharmacy = DataSources.lookup("jdbc/pharmacy");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String patientRef = req.getParameter("patient");
        if (patientRef == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = pharmacy.getConnection();
             CallableStatement cs = conn.prepareCall("{call find_prescriptions(?, ?)}")) {
            cs.setString(1, patientRef.trim());
            cs.setInt(2, 25);
            try (ResultSet rs = cs.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong("rx_id"));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
