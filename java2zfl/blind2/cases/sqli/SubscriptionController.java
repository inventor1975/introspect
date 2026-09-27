package blind2.sqli;

import blind2.sqli.service.SubscriptionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SubscriptionController {

    @Autowired
    private SubscriptionService subscriptions;

    @PutMapping("/api/subscriptions/{id}/plan")
    public ResponseEntity<String> changePlan(@PathVariable long id, @RequestParam String plan) {
        if (plan.isBlank()) {
            return new ResponseEntity<>("plan required", HttpStatus.BAD_REQUEST);
        }
        boolean changed = subscriptions.changePlan(id, plan);
        return changed ? ResponseEntity.ok("updated") : new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
}
