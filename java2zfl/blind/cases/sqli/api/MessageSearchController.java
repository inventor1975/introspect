package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MessageSearchController {

    private final JdbcTemplate jdbc;

    public MessageSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/v2/messages/filter")
    public List<Map<String, Object>> filter(@RequestBody MessageFilter filter) {
        String folder = filter.getFolder() == null ? "INBOX" : filter.getFolder();
        int limit = Math.max(1, Math.min(filter.getLimit(), 500));
        String sql = "SELECT id, subject, received_at FROM messages WHERE folder = ? AND sender = ?"
                + " ORDER BY received_at DESC LIMIT " + limit;
        return jdbc.queryForList(sql, folder, filter.getSender());
    }
}
