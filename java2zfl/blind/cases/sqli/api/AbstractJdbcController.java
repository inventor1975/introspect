package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.jdbc.core.JdbcTemplate;

public abstract class AbstractJdbcController {

    private static final Set<String> FILTERABLE = Set.of("department", "location", "title", "manager_id");

    protected final JdbcTemplate jdbc;

    protected AbstractJdbcController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    protected abstract String table();

    protected List<Map<String, Object>> findBy(String column, String value) {
        return jdbc.queryForList("SELECT * FROM " + table() + " WHERE " + column + " = '" + value + "'");
    }

    protected List<Map<String, Object>> findWhere(String column, String value) {
        if (!FILTERABLE.contains(column)) {
            throw new IllegalArgumentException("column not filterable");
        }
        return jdbc.queryForList("SELECT * FROM " + table() + " WHERE " + column + " = ?", value);
    }
}
