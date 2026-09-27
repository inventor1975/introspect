package blind2.xss.spring;

import java.util.Set;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CategoryController {

    private static final Set<String> CATEGORIES = Set.of("books", "music", "games", "garden");

    @GetMapping("/browse")
    public ResponseEntity<String> browse(@RequestParam("cat") String cat) {
        if (!CATEGORIES.contains(cat)) {
            return ResponseEntity.badRequest().body("<p class=\"error\">Unknown category: " + cat + "</p>");
        }
        return ResponseEntity.ok("<div id=\"list\" data-cat=\"" + cat + "\"></div>");
    }
}
