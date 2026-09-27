package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductListingController {

    private final ProductListingService listingService;

    public ProductListingController(ProductListingService listingService) {
        this.listingService = listingService;
    }

    @PostMapping("/api/v2/products/search")
    public List<Map<String, Object>> search(@RequestBody SearchRequest request) {
        return listingService.list(request);
    }
}
