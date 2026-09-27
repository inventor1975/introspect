package blind2.xss.spring;

import blind2.xss.support.GuestEntry;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class GuestbookController {

    @PostMapping(value = "/guestbook/sign", produces = "text/html")
    @ResponseBody
    public String sign(@ModelAttribute GuestEntry entry) {
        int length = entry.getMessage() == null ? 0 : entry.getMessage().length();
        return "<p>Thanks for signing, " + entry.getDisplayName() + "!</p>"
                + "<p>Your " + length + "-character message is awaiting moderation.</p>";
    }
}
