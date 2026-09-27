package blind.xss.catalog;

import javax.servlet.annotation.WebServlet;
import org.springframework.web.util.HtmlUtils;

@WebServlet("/promo/seasonal")
public class SeasonalPromoServlet extends PromoServletBase {

    @Override
    protected String campaignName() {
        return "Winter sale";
    }

    @Override
    protected String formatCode(String code) {
        return HtmlUtils.htmlEscape(code).replace("\r\n", "\n").replace("\n", "<br>");
    }
}
