package blind.sqli.api;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ColumnPickerController {

    private final JdbcTemplate jdbc;

    public ColumnPickerController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/reports/custom")
    public ResponseEntity<List<Map<String, Object>>> custom(@RequestParam String column) {
        Set<String> exposed = new HashSet<>(jdbc.queryForList(
                "SELECT column_name FROM report_exposed_columns WHERE enabled = TRUE", String.class));
        if (!exposed.contains(column)) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(jdbc.queryForList(
                "SELECT " + column + ", COUNT(*) AS n FROM orders GROUP BY " + column + " ORDER BY n DESC"));
    }
}
