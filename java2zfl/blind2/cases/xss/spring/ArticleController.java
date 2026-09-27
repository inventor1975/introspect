package blind2.xss.spring;

import java.util.Map;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ArticleController {

    private static final Map<String, String> PUBLISHED = Map.of(
            "getting-started", "<h1>Getting started</h1><p>Install the CLI.</p>",
            "faq", "<h1>FAQ</h1><p>Common questions.</p>");

    @GetMapping("/articles/{slug}")
    @ResponseBody
    public String article(@PathVariable("slug") String slug) {
        String body = PUBLISHED.get(slug);
        if (body == null) {
            return "<h1>Not found</h1><p>There is no article named <i>" + slug + "</i>.</p>";
        }
        return body;
    }
}
