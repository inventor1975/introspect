package blind2.xss.spring;

import blind2.xss.support.ContactRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ContactApiController {

    @PostMapping("/api/contact")
    public ResponseEntity<ContactRequest> submit(@RequestBody ContactRequest request) {
        String subject = request.subject() == null ? "(none)" : "[Web] " + request.subject();
        ContactRequest normalized = new ContactRequest(request.name(), request.email(), subject, request.body());
        return ResponseEntity.ok(normalized);
    }
}
