package blind.xss.catalog;

import java.math.BigDecimal;
import java.math.RoundingMode;
import org.owasp.encoder.Encode;

/** Reusable storefront fragments. */
public final class ProductSnippets {

    private ProductSnippets() {
    }

    public static String card(String title, String priceText) {
        return "<div class=\"card\"><h4>" + title + "</h4><span class=\"price\">" + priceText + "</span></div>";
    }

    public static String priceTag(BigDecimal amount) {
        return "<span class=\"price\">$" + amount.setScale(2, RoundingMode.HALF_UP).toPlainString() + "</span>";
    }

    public static String safeCard(String title, BigDecimal price) {
        return "<div class=\"card\"><h4>" + Encode.forHtml(title) + "</h4>" + priceTag(price) + "</div>";
    }
}
