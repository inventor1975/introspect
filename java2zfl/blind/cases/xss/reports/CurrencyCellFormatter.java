package blind.xss.reports;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Locale;

public class CurrencyCellFormatter implements CellFormatter {

    private final NumberFormat currency = NumberFormat.getCurrencyInstance(Locale.US);

    @Override
    public String format(String raw) {
        if (raw == null || raw.isBlank()) {
            return "&ndash;";
        }
        try {
            BigDecimal amount = new BigDecimal(raw.trim());
            return currency.format(amount);
        } catch (NumberFormatException e) {
            return "<span class=\"invalid\">n/a</span>";
        }
    }
}
