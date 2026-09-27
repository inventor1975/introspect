package blind2.xss.spring;

import blind2.xss.support.GreetingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WelcomeController {

    private final GreetingService greetings;

    public WelcomeController(GreetingService greetings) {
        this.greetings = greetings;
    }

    @GetMapping("/fragments/welcome")
    public String welcome(@RequestParam(value = "name", required = false) String name) {
        return greetings.welcome(name) + "<p>Take the tour to learn the basics.</p>";
    }
}
