package blind.xss.common;

import org.owasp.encoder.Encode;

/**
 * Tiny helpers for building HTML fragments in servlets that do not go through the template engine.
 */
public final class Markup {

    private Markup() {
    }

    /** Escapes a value for use as element text. */
    public static String text(String value) {
        return value == null ? "" : Encode.forHtml(value);
    }

    /** Wraps already-rendered markup in an element. */
    public static String tag(String name, String content) {
        return "<" + name + ">" + content + "</" + name + ">";
    }

    /** Renders an anchor; the label is escaped, the href is used as given. */
    public static String link(String href, String label) {
        return "<a href=\"" + href + "\">" + text(label) + "</a>";
    }

    public static String page(String title, String body) {
        return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>" + text(title)
                + "</title><link rel=\"stylesheet\" href=\"/static/site.css\"></head><body>"
                + body + "</body></html>";
    }
}
