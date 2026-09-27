package blind2.xss.spring;

import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReleaseNotesController {

    private final Parser parser = Parser.builder().build();
    private final HtmlRenderer renderer = HtmlRenderer.builder()
            .escapeHtml(true)
            .sanitizeUrls(true)
            .build();

    @PostMapping(value = "/releases/notes/preview", produces = "text/html")
    public String preview(@RequestParam("notes") String notes) {
        return "<section class=\"notes\">" + renderer.render(parser.parse(notes)) + "</section>";
    }
}
