package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CustomerQueryController {

    private static final String CUSTOMER_COLUMNS = "id, first_name, last_name, city";
    private final JdbcTemplate jdbcTemplate;

    public CustomerQueryController(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @GetMapping("/api/v2/customers")
    public List<Map<String, Object>> byLastName(@RequestParam("lastName") String lastName,
                                                @RequestParam(value = "city", required = false) String city) {
        if (city == null) {
            return jdbcTemplate.queryForList(
                    "SELECT " + CUSTOMER_COLUMNS + " FROM customers WHERE last_name = ?", lastName);
        }
        return jdbcTemplate.queryForList(
                "SELECT " + CUSTOMER_COLUMNS + " FROM customers WHERE last_name = ? AND city = ?", lastName, city);
    }
}
