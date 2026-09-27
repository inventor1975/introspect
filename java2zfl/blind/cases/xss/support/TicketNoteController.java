package blind.xss.support;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TicketNoteController {

    @PostMapping(value = "/support/tickets/{id}/notes/preview",
            consumes = MediaType.TEXT_PLAIN_VALUE, produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@PathVariable("id") long ticketId, @RequestBody String note) {
        String html = note.strip().replace("\r\n", "\n").replace("\n", "<br>");
        return "<article class=\"note\" data-ticket=\"" + ticketId + "\">" + html + "</article>";
    }
}
