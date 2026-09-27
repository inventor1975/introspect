package blind2.sqli.data;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

public class JdbcVehicleRepository implements VehicleRepository {

    private final DataSource dataSource;

    public JdbcVehicleRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public List<Vehicle> findByPlatePrefix(String prefix) throws SQLException {
        List<Vehicle> result = new ArrayList<>();
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT vin, plate, model_year FROM fleet_vehicles WHERE plate LIKE ? ORDER BY plate")) {
            ps.setString(1, prefix + "%");
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    result.add(new Vehicle(rs.getString(1), rs.getString(2), rs.getInt(3)));
                }
            }
        }
        return result;
    }
}
