package blind2.xss.spring;

import java.util.Locale;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PriorityController {

    enum Priority { LOW, NORMAL, HIGH, URGENT }

    @GetMapping("/tasks/priority-chip")
    public ResponseEntity<String> chip(@RequestParam("p") String p) {
        Priority priority;
        try {
            priority = Priority.valueOf(p.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body("<span class=\"chip\">invalid</span>");
        }
        String css = priority.name().toLowerCase(Locale.ROOT);
        return ResponseEntity.ok("<span class=\"chip chip-" + css + "\">" + priority + "</span>");
    }
}
