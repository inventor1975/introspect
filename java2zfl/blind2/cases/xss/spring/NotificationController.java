package blind2.xss.spring;

import blind2.xss.support.MessageFormatter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotificationController {

    @Autowired
    private MessageFormatter formatter;

    @GetMapping(value = "/notifications/toast", produces = "text/html")
    public String toast(@RequestParam("item") String item) {
        return "<div class=\"toast\">" + formatter.format("{} was added to your list.", item) + "</div>";
    }
}
