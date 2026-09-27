package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExportController {

    private final JdbcTemplate jdbc;

    public ExportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/export/customers")
    public List<Map<String, Object>> export(@RequestParam(defaultValue = "created_at") String orderBy,
                                            @RequestParam(defaultValue = "asc") String dir) {
        String direction = "desc".equalsIgnoreCase(dir) ? "DESC" : "ASC";
        return jdbc.queryForList("SELECT id, email, created_at, country FROM customers ORDER BY "
                + orderBy + " " + direction);
    }
}
