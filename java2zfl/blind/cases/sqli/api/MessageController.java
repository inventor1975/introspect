package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MessageController {

    private final JdbcTemplate jdbc;

    public MessageController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/messages/filter")
    public List<Map<String, Object>> filter(@RequestBody MessageFilter filter) {
        String folder = filter.getFolder() == null ? "INBOX" : filter.getFolder();
        String sql = "SELECT id, subject, received_at FROM messages WHERE folder = ? AND sender = '"
                + filter.getSender() + "' ORDER BY received_at DESC LIMIT " + filter.getLimit();
        return jdbc.queryForList(sql, folder);
    }
}
