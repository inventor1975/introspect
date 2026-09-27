package blind.xss.support;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MotdController {

    private static final Path MOTD = Path.of("/etc/helpdesk/motd.html");

    @GetMapping(value = "/support/motd", produces = MediaType.TEXT_HTML_VALUE)
    public String motd(@RequestParam(value = "compact", defaultValue = "false") boolean compact) {
        String content;
        try {
            content = Files.readString(MOTD);
        } catch (IOException e) {
            content = "<p>Welcome to the help desk.</p>";
        }
        return "<div class=\"motd" + (compact ? " compact" : "") + "\">" + content + "</div>";
    }
}
