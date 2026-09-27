package blind.sqli.api;

import javax.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchLogController {

    private static final String LOG_TABLE = "search_log";
    private final JdbcTemplate jdbc;

    public SearchLogController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/v2/search/log")
    public ResponseEntity<Void> log(HttpServletRequest request) {
        String term = request.getParameter("q");
        if (term == null || term.length() > 200) {
            return ResponseEntity.badRequest().build();
        }
        jdbc.update("INSERT INTO " + LOG_TABLE + " (term, searched_at) VALUES (?, CURRENT_TIMESTAMP)", term);
        return ResponseEntity.ok().build();
    }
}
