package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotesController {

    private final JdbcTemplate jdbc;

    public NotesController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/notebooks/{notebook}/notes")
    public List<Map<String, Object>> notes(@PathVariable String notebook,
                                           @RequestParam(defaultValue = "20") String limit) {
        int max;
        try {
            max = Math.min(Integer.parseInt(limit), 100);
        } catch (NumberFormatException e) {
            max = 20;
        }
        return jdbc.queryForList("SELECT id, title, updated_at FROM notes WHERE notebook_slug = ?"
                + " ORDER BY updated_at DESC LIMIT " + max, notebook);
    }
}
