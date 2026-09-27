package blind.xss.support;

import org.owasp.encoder.Encode;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TicketPreviewController {

    @PostMapping(value = "/support/tickets/{id}/reply/preview",
            consumes = MediaType.TEXT_PLAIN_VALUE, produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@PathVariable("id") long ticketId, @RequestBody String reply) {
        String html = Encode.forHtml(reply.strip()).replace("\r\n", "\n").replace("\n", "<br>");
        return "<article class=\"reply\" data-ticket=\"" + ticketId + "\">" + html + "</article>";
    }
}
