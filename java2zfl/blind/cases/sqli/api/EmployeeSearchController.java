package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EmployeeSearchController extends AbstractJdbcController {

    public EmployeeSearchController(JdbcTemplate jdbc) {
        super(jdbc);
    }

    @Override
    protected String table() {
        return "employees";
    }

    @GetMapping("/api/v2/employees/by-location")
    public List<Map<String, Object>> byLocation(@RequestParam String location) {
        return findWhere("location", location);
    }
}
