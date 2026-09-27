package blind2.xss.support;

import org.springframework.stereotype.Service;
import org.springframework.web.util.HtmlUtils;

@Service
public class GreetingService {

    public String banner(String displayName) {
        String who = displayName == null ? "friend" : displayName.trim();
        return "<div class=\"banner\">Good to see you, " + who + "</div>";
    }

    public String welcome(String displayName) {
        String who = displayName == null ? "friend" : displayName.trim();
        return "<div class=\"banner\">Welcome aboard, " + HtmlUtils.htmlEscape(who) + "</div>";
    }
}
