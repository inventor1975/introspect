package blind2.xss.spring;

import org.owasp.html.PolicyFactory;
import org.owasp.html.Sanitizers;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ForumReplyController {

    private static final PolicyFactory POLICY = Sanitizers.FORMATTING.and(Sanitizers.LINKS).and(Sanitizers.BLOCKS);

    @PostMapping("/forum/reply/preview")
    public ResponseEntity<String> preview(@RequestParam("html") String html) {
        String safeHtml = POLICY.sanitize(html);
        return ResponseEntity.ok()
                .contentType(MediaType.TEXT_HTML)
                .body("<div class=\"reply\">" + safeHtml + "</div>");
    }
}
