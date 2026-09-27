package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

class DirectReportsQuery implements OrgQuery {
    @Override
    public List<Map<String, Object>> run(JdbcTemplate jdbc, long employeeId) {
        return jdbc.queryForList("SELECT id, name FROM employees WHERE manager_id = ? ORDER BY name", employeeId);
    }
}
