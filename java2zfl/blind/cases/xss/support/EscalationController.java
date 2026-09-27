package blind.xss.support;

import java.util.Locale;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EscalationController {

    enum Priority { LOW, NORMAL, HIGH, URGENT }

    @PostMapping("/support/tickets/{id}/escalate")
    public ResponseEntity<String> escalate(@PathVariable("id") long id, @RequestParam("priority") String priority) {
        Priority target;
        try {
            target = Priority.valueOf(priority.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().contentType(MediaType.TEXT_HTML)
                    .body("<p class=\"error\">Unknown priority '" + priority + "'.</p>");
        }
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML)
                .body("<p>Ticket " + id + " escalated to " + target.name().toLowerCase(Locale.ROOT) + ".</p>");
    }
}
