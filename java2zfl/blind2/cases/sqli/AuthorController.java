package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/authors")
public class AuthorController {

    private final JdbcTemplate jdbc;

    public AuthorController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping
    public List<Map<String, Object>> search(@RequestParam("q") String query) {
        String pattern = "%" + query.trim() + "%";
        return jdbc.queryForList("SELECT id, name, country FROM authors WHERE name ILIKE ? ORDER BY name LIMIT 50", pattern);
    }

    @GetMapping("/{slug}/books")
    public List<String> books(@PathVariable String slug) {
        return jdbc.queryForList(
                "SELECT b.title FROM books b JOIN authors a ON a.id = b.author_id WHERE a.slug = ? ORDER BY b.published_on",
                String.class, slug);
    }
}
