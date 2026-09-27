package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SortPreferenceController {

    private final JdbcTemplate jdbc;
    private volatile String defaultSort = "created_at DESC";

    public SortPreferenceController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/admin/listing/default-sort")
    public ResponseEntity<Void> setDefaultSort(@RequestParam String sort) {
        this.defaultSort = sort;
        return ResponseEntity.ok().build();
    }

    @GetMapping("/api/listings")
    public List<Map<String, Object>> listings() {
        return jdbc.queryForList("SELECT id, title, price, created_at FROM listings WHERE published = TRUE ORDER BY "
                + defaultSort + " LIMIT 100");
    }
}
