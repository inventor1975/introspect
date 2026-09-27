package blind2.xss.spring;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InvitationController {

    @GetMapping("/invite")
    public ResponseEntity<String> invite(@RequestParam("inviter") String inviter,
                                         @RequestParam("team") String team) {
        String page = String.format(
                "<html><body><h2>%s invited you to join %s</h2><a href=\"/signup\">Accept</a></body></html>",
                inviter, team);
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(page);
    }
}
