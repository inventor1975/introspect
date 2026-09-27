package blind2.sqli;

import blind2.sqli.model.ThreadSort;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ForumThreadController {

    private final JdbcTemplate jdbc;

    public ForumThreadController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/forums/{forumId}/threads")
    public List<Map<String, Object>> threads(@PathVariable long forumId,
                                             @RequestParam(value = "sort", defaultValue = "NEWEST") ThreadSort sort) {
        String sql = "SELECT t.id, t.title, t.reply_count FROM forum_threads t WHERE t.forum_id = ? AND t.hidden = false"
                + " ORDER BY " + sort.orderBy() + " LIMIT 30";
        return jdbc.queryForList(sql, forumId);
    }
}
