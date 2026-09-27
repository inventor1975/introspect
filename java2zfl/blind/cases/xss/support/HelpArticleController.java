package blind.xss.support;

import java.lang.reflect.Method;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelpArticleController {

    public static class HelpArticle {
        private final String title;
        private final String summary;
        private final String body;

        public HelpArticle(String title, String summary, String body) {
            this.title = title;
            this.summary = summary;
            this.body = body;
        }

        public String getTitle() {
            return title;
        }

        public String getSummary() {
            return summary;
        }

        public String getBody() {
            return body;
        }
    }

    @PostMapping(value = "/help/articles/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("title") String title,
                          @RequestParam("summary") String summary,
                          @RequestParam("body") String body,
                          @RequestParam(value = "section", defaultValue = "summary") String section)
            throws ReflectiveOperationException {
        HelpArticle draft = new HelpArticle(title, summary, body);
        String getter = "get" + Character.toUpperCase(section.charAt(0)) + section.substring(1);
        Method accessor = HelpArticle.class.getMethod(getter);
        Object value = accessor.invoke(draft);
        return "<div class=\"help-preview section-" + section.length() + "\">" + value + "</div>";
    }
}
