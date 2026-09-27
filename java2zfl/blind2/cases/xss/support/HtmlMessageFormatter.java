package blind2.xss.support;

import org.springframework.stereotype.Component;
import org.springframework.web.util.HtmlUtils;

@Component
public class HtmlMessageFormatter implements MessageFormatter {
    @Override
    public String format(String template, String subject) {
        return template.replace("{}", HtmlUtils.htmlEscape(subject == null ? "" : subject));
    }
}
