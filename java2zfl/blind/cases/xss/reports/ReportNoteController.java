package blind.xss.reports;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportNoteController {

    private final JdbcTemplate jdbc;

    public ReportNoteController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/reports/{id}/note")
    public ResponseEntity<String> saveNote(@PathVariable("id") long id, @RequestParam("note") String note) {
        jdbc.update("UPDATE reports SET note = ? WHERE id = ?", note, id);
        return ResponseEntity.ok().contentType(MediaType.TEXT_PLAIN).body("saved");
    }

    @GetMapping(value = "/reports/{id}", produces = MediaType.TEXT_HTML_VALUE)
    public String show(@PathVariable("id") long id) {
        String note = jdbc.queryForObject("SELECT note FROM reports WHERE id = ?", String.class, id);
        return "<section class=\"report\"><h2>Report " + id + "</h2>"
                + "<div class=\"note\">" + (note == null ? "" : note) + "</div></section>";
    }
}
