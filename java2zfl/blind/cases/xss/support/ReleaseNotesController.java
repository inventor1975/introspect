package blind.xss.support;

import org.commonmark.node.Node;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReleaseNotesController {

    private static final Parser PARSER = Parser.builder().build();
    private static final HtmlRenderer RENDERER = HtmlRenderer.builder().build();

    @PostMapping(value = "/support/release-notes/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("markdown") String markdown) {
        Node document = PARSER.parse(markdown);
        return "<article class=\"release-notes\">" + RENDERER.render(document) + "</article>";
    }
}
