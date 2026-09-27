package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/books")
public class BookSearchController {

    private final JdbcTemplate jdbc;

    public BookSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/search")
    public List<Map<String, Object>> search(@RequestParam("title") String title,
                                            @RequestParam(value = "limit", defaultValue = "20") int limit) {
        int capped = Math.min(Math.max(limit, 1), 100);
        return jdbc.queryForList("SELECT isbn, title, author FROM books WHERE lower(title) LIKE lower('%" + title
                + "%') ORDER BY title LIMIT " + capped);
    }
}
