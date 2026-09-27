package blind2.sqli.data;

import java.sql.SQLException;
import java.util.List;

public interface VehicleRepository {

    List<Vehicle> findByPlatePrefix(String prefix) throws SQLException;
}
