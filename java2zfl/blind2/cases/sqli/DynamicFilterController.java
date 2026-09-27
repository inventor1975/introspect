package blind2.sqli;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DynamicFilterController {

    private static final Set<String> RESERVED = Set.of("page", "size");

    private final JdbcTemplate jdbc;

    public DynamicFilterController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/assets")
    public List<Map<String, Object>> list(@RequestParam Map<String, String> filters) {
        String where = filters.entrySet().stream()
                .filter(e -> !RESERVED.contains(e.getKey()))
                .map(e -> e.getKey() + " = '" + e.getValue() + "'")
                .collect(Collectors.joining(" AND "));
        String sql = "SELECT id, asset_tag, location FROM assets" + (where.isEmpty() ? "" : " WHERE " + where)
                + " ORDER BY asset_tag LIMIT 200";
        return jdbc.queryForList(sql);
    }
}
