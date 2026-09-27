package blind.xss.account;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SettingsSaveController {

    private static final int MIN_LENGTH = 3;
    private static final int MAX_LENGTH = 40;

    @PostMapping(value = "/account/settings/validate", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> validate(@RequestParam("displayName") String displayName) {
        String trimmed = displayName.trim();
        boolean valid = trimmed.length() >= MIN_LENGTH && trimmed.length() <= MAX_LENGTH;
        String json = "{\"valid\":" + valid + ",\"length\":" + trimmed.length() + ",\"max\":" + MAX_LENGTH + "}";
        return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(json);
    }
}
