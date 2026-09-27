package blind.sqli.api;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CommentModerationController {

    private final JdbcTemplate jdbc;

    public CommentModerationController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/moderation/hide")
    public ResponseEntity<Integer> hide(@RequestBody List<String> commentIds) {
        String[] statements = new String[commentIds.size()];
        for (int i = 0; i < commentIds.size(); i++) {
            statements[i] = "UPDATE comments SET hidden = TRUE, hidden_at = CURRENT_TIMESTAMP WHERE id = " + commentIds.get(i);
        }
        int[] counts = jdbc.batchUpdate(statements);
        return ResponseEntity.ok(counts.length);
    }
}
