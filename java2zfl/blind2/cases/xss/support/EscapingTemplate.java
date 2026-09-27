package blind2.xss.support;

import java.util.Map;
import org.owasp.encoder.Encode;

public final class EscapingTemplate {

    private final String source;

    public EscapingTemplate(String source) {
        this.source = source;
    }

    public String fill(Map<String, String> values) {
        String result = source;
        for (Map.Entry<String, String> e : values.entrySet()) {
            String v = e.getValue() == null ? "" : e.getValue();
            result = result.replace("{{" + e.getKey() + "}}", Encode.forHtml(v));
        }
        return result;
    }
}
