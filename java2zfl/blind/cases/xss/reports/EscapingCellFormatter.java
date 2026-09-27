package blind.xss.reports;

import org.owasp.encoder.Encode;

public class EscapingCellFormatter implements CellFormatter {
    @Override
    public String format(String raw) {
        return raw == null ? "" : Encode.forHtml(raw);
    }
}
