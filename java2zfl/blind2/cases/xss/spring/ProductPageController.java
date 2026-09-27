package blind2.xss.spring;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class ProductPageController {

    @GetMapping("/products/{id}")
    public String product(@PathVariable("id") long id,
                          @RequestParam(value = "highlight", required = false) String highlight,
                          @RequestParam(value = "ref", required = false) String ref,
                          Model model) {
        model.addAttribute("productId", id);
        model.addAttribute("highlight", highlight);
        model.addAttribute("ref", ref);
        return "product/detail";
    }
}
