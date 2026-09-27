package blind.sqli.api;

import blind.sqli.support.SqlFragments;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AccountController {

    private final JdbcTemplate jdbc;

    public AccountController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/accounts/search")
    public List<Map<String, Object>> search(@RequestParam String name) {
        String sql = "SELECT id, company_name, owner_email FROM accounts WHERE company_name ILIKE "
                + SqlFragments.like(name) + " ORDER BY company_name LIMIT 50";
        return jdbc.queryForList(sql);
    }
}
