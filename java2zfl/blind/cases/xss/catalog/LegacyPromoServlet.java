package blind.xss.catalog;

import javax.servlet.annotation.WebServlet;

@WebServlet("/promo/legacy")
public class LegacyPromoServlet extends PromoServletBase {

    @Override
    protected String campaignName() {
        return "Loyalty rewards (classic)";
    }

    /** Codes from the old loyalty system can span several lines. */
    @Override
    protected String formatCode(String code) {
        return code.replace("\r\n", "\n").replace("\n", "<br>");
    }
}
