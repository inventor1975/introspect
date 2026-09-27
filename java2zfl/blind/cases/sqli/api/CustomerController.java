package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CustomerController {

    private final JdbcTemplate jdbcTemplate;

    public CustomerController(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @GetMapping("/api/customers")
    public List<Map<String, Object>> byLastName(@RequestParam("lastName") String lastName) {
        return jdbcTemplate.queryForList(
                "SELECT id, first_name, last_name, city FROM customers WHERE last_name = '" + lastName + "'");
    }
}
