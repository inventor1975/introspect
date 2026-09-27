package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

class ManagerChainQuery implements OrgQuery {
    @Override
    public List<Map<String, Object>> run(JdbcTemplate jdbc, long employeeId) {
        return jdbc.queryForList(
                "WITH RECURSIVE chain AS (SELECT id, manager_id, name FROM employees WHERE id = ?"
                        + " UNION ALL SELECT e.id, e.manager_id, e.name FROM employees e JOIN chain c ON e.id = c.manager_id)"
                        + " SELECT id, name FROM chain", employeeId);
    }
}
