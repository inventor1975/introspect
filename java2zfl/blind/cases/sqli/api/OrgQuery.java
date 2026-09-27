package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

public interface OrgQuery {

    List<Map<String, Object>> run(JdbcTemplate jdbc, long employeeId);
}
