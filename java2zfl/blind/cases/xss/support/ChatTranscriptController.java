package blind.xss.support;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatTranscriptController {

    @PostMapping(value = "/support/chat/transcript", produces = MediaType.TEXT_HTML_VALUE)
    public String transcript(@RequestParam("line") List<String> lines,
                             @RequestParam(value = "customer", defaultValue = "Customer") String customer) {
        String body = lines.stream()
                .filter(l -> !l.isBlank())
                .map(l -> "<p class=\"msg\"><b>" + customer + ":</b> " + l + "</p>")
                .collect(Collectors.joining("\n"));
        return "<div class=\"transcript\">" + body + "</div>";
    }
}
