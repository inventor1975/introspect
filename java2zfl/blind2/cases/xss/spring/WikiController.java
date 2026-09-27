package blind2.xss.spring;

import org.commonmark.node.Node;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WikiController {

    private final Parser parser = Parser.builder().build();
    private final HtmlRenderer renderer = HtmlRenderer.builder().build();

    @PostMapping(value = "/wiki/preview", produces = "text/html")
    public String preview(@RequestParam("source") String source) {
        Node document = parser.parse(source);
        return "<div class=\"wiki-page\">" + renderer.render(document) + "</div>";
    }
}
