package blind.xss.support;

import java.util.Locale;
import org.owasp.encoder.Encode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EscalationStatusController {

    enum Priority { LOW, NORMAL, HIGH, URGENT }

    @GetMapping("/support/tickets/{id}/escalation")
    public ResponseEntity<String> status(@PathVariable("id") long id, @RequestParam("priority") String priority) {
        Priority target;
        try {
            target = Priority.valueOf(priority.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().contentType(MediaType.TEXT_HTML)
                    .body("<p class=\"error\">Unknown priority '" + Encode.forHtml(priority) + "'.</p>");
        }
        String note = target == Priority.URGENT ? "An on-call engineer has been paged." : "The team will reply shortly.";
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML)
                .body("<p>Ticket " + id + " is marked " + target.name().toLowerCase(Locale.ROOT) + ". " + note + "</p>");
    }
}
