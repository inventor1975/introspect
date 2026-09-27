package blind2.sqli;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotificationController {

    private static final Function<String, String> UNREAD_FOR = recipient ->
            "SELECT id, title, created_at FROM notifications WHERE recipient = '" + recipient
                    + "' AND read_at IS NULL ORDER BY created_at DESC";

    private final JdbcTemplate jdbc;

    public NotificationController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/notifications/unread")
    public List<Map<String, Object>> unread(@RequestParam("user") String user) {
        return jdbc.queryForList(UNREAD_FOR.apply(user));
    }
}
