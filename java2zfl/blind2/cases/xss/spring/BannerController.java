package blind2.xss.spring;

import blind2.xss.support.GreetingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BannerController {

    private final GreetingService greetings;

    public BannerController(GreetingService greetings) {
        this.greetings = greetings;
    }

    @GetMapping("/fragments/banner")
    public String banner(@RequestParam(value = "name", required = false) String name) {
        return greetings.banner(name);
    }
}
