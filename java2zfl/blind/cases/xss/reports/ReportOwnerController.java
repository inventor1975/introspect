package blind.xss.reports;

import org.owasp.encoder.Encode;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportOwnerController {

    private final JdbcTemplate jdbc;

    public ReportOwnerController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping(value = "/reports/{id}/owner", produces = MediaType.TEXT_HTML_VALUE)
    public String owner(@PathVariable("id") long id) {
        String owner = jdbc.queryForObject("SELECT owner_name FROM reports WHERE id = ?", String.class, id);
        String team = jdbc.queryForObject("SELECT team FROM reports WHERE id = ?", String.class, id);
        return "<p class=\"owner\">Owned by <b>" + Encode.forHtml(owner) + "</b> (" + Encode.forHtml(team) + ")</p>";
    }
}
