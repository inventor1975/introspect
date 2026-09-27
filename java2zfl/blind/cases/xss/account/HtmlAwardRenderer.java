package blind.xss.account;

import org.springframework.stereotype.Component;

/** Award labels are authored in the admin console and may carry inline markup such as icons. */
@Component
public class HtmlAwardRenderer implements AwardRenderer {
    @Override
    public String render(String label, String tier) {
        return "<span class=\"award award-" + tier + "\">" + label + "</span>";
    }
}
