package blind.xss.catalog;

import java.util.Arrays;
import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CategoryTreeController {

    @GetMapping(value = "/catalog/tree", produces = MediaType.TEXT_HTML_VALUE)
    public String tree(@RequestParam("path") String path) {
        List<String> segments = Arrays.asList(path.split("/"));
        return "<nav class=\"tree\">" + renderLevel(segments, 0) + "</nav>";
    }

    private String renderLevel(List<String> segments, int depth) {
        if (depth >= segments.size()) {
            return "";
        }
        String name = segments.get(depth);
        if (name.isEmpty()) {
            return renderLevel(segments, depth + 1);
        }
        return "<ul><li class=\"depth-" + depth + "\">" + name + renderLevel(segments, depth + 1) + "</li></ul>";
    }
}
