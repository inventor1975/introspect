package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductSearchController {

    private final ProductSearchService searchService;

    public ProductSearchController(ProductSearchService searchService) {
        this.searchService = searchService;
    }

    @PostMapping("/api/products/search")
    public List<Map<String, Object>> search(@RequestBody SearchRequest request) {
        return searchService.search(request);
    }
}
