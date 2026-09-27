package blind2.xss.spring;

import blind2.xss.support.SearchForm;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class AdvancedSearchController {

    @GetMapping("/search/advanced")
    @ResponseBody
    public String results(@ModelAttribute SearchForm form) {
        String category = form.getCategory() == null ? "all categories" : form.getCategory();
        return "<div class=\"summary\">Page " + form.getPage() + " of results for <b>"
                + form.getQuery() + "</b> in " + category + "</div>";
    }
}
