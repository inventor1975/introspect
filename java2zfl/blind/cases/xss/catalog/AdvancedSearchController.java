package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class AdvancedSearchController {

    @GetMapping(value = "/catalog/advanced", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public String advanced(@ModelAttribute SearchForm form) {
        StringBuilder summary = new StringBuilder("<p class=\"summary\">Showing ");
        if (form.getBrand() != null && !form.getBrand().isEmpty()) {
            summary.append(form.getBrand()).append(' ');
        }
        summary.append("products");
        if (form.getKeyword() != null) {
            summary.append(" matching <em>").append(form.getKeyword()).append("</em>");
        }
        if (form.getMaxPrice() > 0) {
            summary.append(" under $").append(form.getMaxPrice());
        }
        summary.append(form.isInStockOnly() ? " (in stock only)" : "").append("</p>");
        return summary.toString();
    }
}
