package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExportSortController {

    private final JdbcTemplate jdbc;

    public ExportSortController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/export/customers")
    public List<Map<String, Object>> export(@RequestParam(defaultValue = "created") String orderBy,
                                            @RequestParam(defaultValue = "asc") String dir) {
        String column = switch (orderBy.toLowerCase()) {
            case "email" -> "email";
            case "country" -> "country";
            case "id" -> "id";
            default -> "created_at";
        };
        String direction = "desc".equalsIgnoreCase(dir) ? "DESC" : "ASC";
        return jdbc.queryForList("SELECT id, email, created_at, country FROM customers ORDER BY "
                + column + " " + direction);
    }
}
