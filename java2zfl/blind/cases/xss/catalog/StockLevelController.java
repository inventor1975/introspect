package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StockLevelController {

    private final InventoryService inventoryService;

    public StockLevelController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @GetMapping("/inventory/level")
    public ResponseEntity<String> level(@RequestParam("qty") String qtyText) {
        int quantity;
        try {
            quantity = Integer.parseInt(qtyText.trim());
        } catch (NumberFormatException e) {
            return ResponseEntity.badRequest().contentType(MediaType.TEXT_HTML).body("<p>Quantity must be a number.</p>");
        }
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML)
                .body("<div class=\"inventory\">" + inventoryService.describeLevel(quantity) + "</div>");
    }
}
