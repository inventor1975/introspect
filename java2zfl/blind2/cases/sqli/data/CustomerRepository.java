package blind2.sqli.data;

import java.sql.SQLException;
import java.util.Optional;

public interface CustomerRepository {

    Optional<CustomerRecord> findByEmail(String email) throws SQLException;

    Optional<CustomerRecord> findById(long id) throws SQLException;
}
