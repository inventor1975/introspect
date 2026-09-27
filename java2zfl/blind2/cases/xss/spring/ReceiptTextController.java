package blind2.xss.spring;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReceiptTextController {

    @GetMapping("/receipts/text")
    public ResponseEntity<String> receipt(@RequestParam("customer") String customer,
                                          @RequestParam("ref") String ref) {
        String text = "RECEIPT\n"
                + "Customer: " + customer + "\n"
                + "Reference: " + ref + "\n"
                + "Thank you for your purchase.\n";
        return ResponseEntity.ok()
                .contentType(MediaType.TEXT_PLAIN)
                .header("X-Content-Type-Options", "nosniff")
                .header("Content-Disposition", "inline; filename=receipt.txt")
                .body(text);
    }
}
