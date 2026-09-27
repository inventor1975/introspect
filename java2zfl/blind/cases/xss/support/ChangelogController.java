package blind.xss.support;

import org.commonmark.node.Node;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChangelogController {

    private final Parser parser = Parser.builder().build();
    private final HtmlRenderer renderer = HtmlRenderer.builder()
            .escapeHtml(true)
            .sanitizeUrls(true)
            .build();

    @PostMapping(value = "/support/changelog/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("markdown") String markdown) {
        Node document = parser.parse(markdown);
        return "<article class=\"changelog\">" + renderer.render(document) + "</article>";
    }
}
