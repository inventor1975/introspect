package blind.sqli.api;

import javax.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchHistoryController {

    private final JdbcTemplate jdbc;

    public SearchHistoryController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/search/log")
    public ResponseEntity<Void> log(HttpServletRequest request) {
        String term = request.getParameter("q");
        if (term == null || term.length() > 200) {
            return ResponseEntity.badRequest().build();
        }
        jdbc.execute("INSERT INTO search_log (term, searched_at) VALUES ('" + term + "', CURRENT_TIMESTAMP)");
        return ResponseEntity.ok().build();
    }
}
