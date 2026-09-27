package blind2.xss.spring;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SkuController {

    private static final Map<String, Integer> STOCK = Map.of("A-100", 4, "A-200", 0, "B-310", 17);

    @GetMapping(value = "/stock/{sku}", produces = "text/html")
    public String stock(@PathVariable("sku") String sku) {
        Integer qty = STOCK.get(sku);
        if (qty == null) {
            throw new IllegalArgumentException("Unknown SKU " + sku);
        }
        return "<span class=\"stock\">" + qty + " in stock</span>";
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<String> onBadSku(IllegalArgumentException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .contentType(MediaType.TEXT_HTML)
                .body("<div class=\"error\">" + ex.getMessage() + "</div>");
    }
}
