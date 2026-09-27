package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PagedCatalogController {

    private final JdbcTemplate jdbc;

    public PagedCatalogController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/catalog")
    public List<Map<String, Object>> page(@RequestParam(value = "page", defaultValue = "0") int page,
                                          @RequestParam(value = "size", defaultValue = "20") int size,
                                          @RequestParam(value = "category", required = false) String category) {
        int limit = Math.min(Math.max(size, 1), 100);
        int offset = Math.max(page, 0) * limit;
        String paging = " ORDER BY id LIMIT " + limit + " OFFSET " + offset;
        if (category == null) {
            return jdbc.queryForList("SELECT id, name FROM products WHERE active = true" + paging);
        }
        return jdbc.queryForList("SELECT id, name FROM products WHERE active = true AND category_code = ?" + paging, category);
    }
}
