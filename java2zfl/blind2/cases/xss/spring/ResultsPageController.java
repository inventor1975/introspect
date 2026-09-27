package blind2.xss.spring;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class ResultsPageController {

    @GetMapping("/search")
    public String search(@RequestParam(value = "q", defaultValue = "") String q, Model model) {
        model.addAttribute("summary", "Showing results for <b>" + q + "</b>");
        model.addAttribute("hits", java.util.List.of());
        return "search/results";
    }
}
