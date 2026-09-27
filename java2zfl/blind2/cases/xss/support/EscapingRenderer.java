package blind2.xss.support;

import org.apache.commons.text.StringEscapeUtils;

public class EscapingRenderer implements Renderer {
    @Override
    public String render(String text) {
        return text == null ? "" : StringEscapeUtils.escapeHtml4(text);
    }
}
