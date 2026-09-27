package blind.xss.catalog;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InventoryController {

    @Autowired
    private InventoryService inventoryService;

    @GetMapping(value = "/inventory/status", produces = MediaType.TEXT_HTML_VALUE)
    public String status(@RequestParam("sku") String sku) {
        String line = inventoryService.describe(sku.trim());
        return "<div class=\"inventory\">" + line + "</div>";
    }
}
