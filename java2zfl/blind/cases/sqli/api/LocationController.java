package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LocationController {

    private static final String STORES_BY_CITY =
            "SELECT id, name, street, opening_hours FROM stores WHERE city = '%s' AND country = '%s' ORDER BY name";

    private final JdbcTemplate jdbc;

    public LocationController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/stores")
    public List<Map<String, Object>> stores(@RequestParam String city,
                                            @RequestParam(defaultValue = "DE") String country) {
        return jdbc.queryForList(String.format(STORES_BY_CITY, city, country.toUpperCase()));
    }
}
