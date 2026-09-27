package blind2.xss.support;

import java.util.Map;

/** Tiny {{name}} substitution used for e-mail and landing snippets. */
public final class PlaceholderTemplate {

    private final String source;

    public PlaceholderTemplate(String source) {
        this.source = source;
    }

    public String fill(Map<String, String> values) {
        String result = source;
        for (Map.Entry<String, String> e : values.entrySet()) {
            result = result.replace("{{" + e.getKey() + "}}", e.getValue() == null ? "" : e.getValue());
        }
        return result;
    }
}
