package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.owasp.esapi.ESAPI;
import org.owasp.esapi.codecs.MySQLCodec;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VendorSearchController {

    private static final MySQLCodec MYSQL = new MySQLCodec(MySQLCodec.Mode.STANDARD);

    private final JdbcTemplate jdbc;

    public VendorSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/vendors/by-contact")
    public List<Map<String, Object>> byContact(@RequestParam String email) {
        String encodedEmail = ESAPI.encoder().encodeForSQL(MYSQL, email);
        return jdbc.queryForList("SELECT id, name, status FROM vendors WHERE contact_email = '" + encodedEmail + "'");
    }
}
