package blind.sqli.api;

import blind.sqli.support.SqlFragments;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AccountSearchController {

    private final JdbcTemplate jdbc;

    public AccountSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/accounts/search")
    public List<Map<String, Object>> search(@RequestParam String name) {
        String sql = "SELECT id, company_name, owner_email FROM accounts WHERE LOWER(company_name) LIKE ?"
                + " ORDER BY company_name LIMIT 50";
        return jdbc.queryForList(sql, SqlFragments.likeParam(name));
    }
}
