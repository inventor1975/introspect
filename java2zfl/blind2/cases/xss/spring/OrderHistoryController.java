package blind2.xss.spring;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class OrderHistoryController {

    @GetMapping("/orders/history")
    public ModelAndView history(@RequestParam(value = "filter", required = false) String filter) {
        return new ModelAndView("orders/history", "filter", filter == null ? "" : filter.trim());
    }
}
