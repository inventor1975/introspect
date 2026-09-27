package blind.xss.account;

import org.owasp.encoder.Encode;

public class TextAwardRenderer implements AwardRenderer {
    @Override
    public String render(String label, String tier) {
        return "<span class=\"award award-" + Encode.forHtmlAttribute(tier) + "\">" + Encode.forHtml(label) + "</span>";
    }
}
