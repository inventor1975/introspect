package blind2.xss.spring;

import java.util.Optional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AliasController {

    @GetMapping("/chat/join")
    public String join(@RequestParam(value = "alias", required = false) String alias) {
        String shown = Optional.ofNullable(alias)
                .map(String::strip)
                .filter(a -> !a.isEmpty() && a.length() <= 64)
                .orElse("guest");
        return "<div class=\"system\">" + shown + " joined the room</div>";
    }
}
