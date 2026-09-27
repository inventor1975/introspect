package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

class PeersQuery implements OrgQuery {
    @Override
    public List<Map<String, Object>> run(JdbcTemplate jdbc, long employeeId) {
        return jdbc.queryForList("SELECT p.id, p.name FROM employees e JOIN employees p ON p.manager_id = e.manager_id"
                + " WHERE e.id = " + employeeId + " AND p.id <> " + employeeId);
    }
}
