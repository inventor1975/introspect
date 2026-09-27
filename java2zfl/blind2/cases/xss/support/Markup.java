package blind2.xss.support;

import org.owasp.encoder.Encode;
import org.springframework.web.util.HtmlUtils;

public final class Markup {

    private Markup() {
    }

    public static String text(String value) {
        if (value == null) {
            return "";
        }
        return HtmlUtils.htmlEscape(value);
    }

    /** Numbers, dates and pre-rendered fragments. */
    public static String text(Object value) {
        return value == null ? "" : String.valueOf(value);
    }

    public static String fragment(String value, boolean escape) {
        if (value == null) {
            return "";
        }
        return escape ? Encode.forHtml(value) : value;
    }
}
