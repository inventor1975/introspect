package blind.xss.account;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileCardController {

    @GetMapping("/account/card")
    public ResponseEntity<String> card(@CookieValue(value = "display_name", defaultValue = "Member") String displayName,
                                       @CookieValue(value = "member_since", defaultValue = "2024") String since) {
        int year;
        try {
            year = Integer.parseInt(since);
        } catch (NumberFormatException e) {
            year = 2024;
        }
        String html = "<div class=\"profile-card\">"
                + "<span class=\"name\">" + displayName + "</span>"
                + "<span class=\"since\">Member since " + year + "</span>"
                + "</div>";
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(html);
    }
}
