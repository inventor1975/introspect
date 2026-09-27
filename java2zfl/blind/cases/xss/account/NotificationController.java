package blind.xss.account;

import java.util.Arrays;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotificationController {

    enum Channel {
        EMAIL("e-mail"), SMS("text message"), PUSH("push notification");

        private final String title;

        Channel(String title) {
            this.title = title;
        }

        String title() {
            return title;
        }
    }

    @GetMapping(value = "/account/notifications/confirm", produces = MediaType.TEXT_HTML_VALUE)
    public String confirm(@RequestParam("channel") String channel) {
        String title = Arrays.stream(Channel.values())
                .filter(c -> c.name().equalsIgnoreCase(channel))
                .findFirst()
                .map(Channel::title)
                .orElse("your default channel");
        return "<p>From now on you will be notified by " + title + ".</p>";
    }
}
