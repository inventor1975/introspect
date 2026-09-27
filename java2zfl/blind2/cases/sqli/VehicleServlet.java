package blind2.sqli;

import blind2.sqli.data.JdbcVehicleRepository;
import blind2.sqli.data.Vehicle;
import blind2.sqli.data.VehicleRepository;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/fleet/vehicles")
public class VehicleServlet extends HttpServlet {

    private VehicleRepository vehicles;

    @Override
    public void init() throws ServletException {
        vehicles = new JdbcVehicleRepository(DataSources.lookup("jdbc/fleet"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String plate = req.getParameter("plate");
        if (plate == null || plate.isBlank()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        List<Vehicle> found;
        try {
            found = vehicles.findByPlatePrefix(plate.trim().toUpperCase());
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        for (Vehicle v : found) {
            out.println(v.modelYear());
        }
    }
}
