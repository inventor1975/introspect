package blind.xss.account;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SettingsController {

    @PostMapping("/account/settings")
    public ResponseEntity<String> save(@RequestParam("displayName") String displayName,
                                       @RequestParam(value = "newsletter", defaultValue = "false") boolean newsletter) {
        if (displayName.length() > 60) {
            return new ResponseEntity<>("<p class=\"error\">Display name is too long.</p>", HttpStatus.BAD_REQUEST);
        }
        String message = "<p>Saved. You will appear as " + displayName + "."
                + (newsletter ? " You are subscribed to the newsletter." : "") + "</p>";
        return new ResponseEntity<>(message, HttpStatus.OK);
    }
}
