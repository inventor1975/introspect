package blind.xss.support;

import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ChatNoticeController {

    @PostMapping(value = "/support/chat/notice", produces = MediaType.TEXT_HTML_VALUE)
    public String notice(@RequestParam("line") List<String> lines) {
        long count = lines.stream().filter(l -> !l.isBlank()).count();
        String first = lines.isEmpty() ? "" : HtmlUtils.htmlEscape(lines.get(0));
        return "<p class=\"notice\">" + count + " new message(s). Latest: <q>" + first + "</q></p>";
    }
}
