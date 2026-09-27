package blind2.sqli;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class JobPostingController {

    private final JdbcTemplate jdbc;

    public JobPostingController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/jobs")
    public List<Map<String, Object>> search(@RequestParam(value = "title", required = false) String title,
                                            @RequestParam(value = "city", required = false) String city,
                                            @RequestParam(value = "remote", required = false) Boolean remote) {
        StringBuilder sql = new StringBuilder("SELECT id, title, city, remote FROM job_postings WHERE open = true");
        List<Object> args = new ArrayList<>();
        if (title != null && !title.isBlank()) {
            sql.append(" AND title ILIKE ?");
            args.add("%" + title.trim() + "%");
        }
        if (city != null && !city.isBlank()) {
            sql.append(" AND city = ?");
            args.add(city.trim());
        }
        if (remote != null) {
            sql.append(" AND remote = ?");
            args.add(remote);
        }
        sql.append(" ORDER BY posted_at DESC LIMIT 50");
        return jdbc.queryForList(sql.toString(), args.toArray());
    }
}
