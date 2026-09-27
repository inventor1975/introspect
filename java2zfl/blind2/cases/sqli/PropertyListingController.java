package blind2.sqli;

import blind2.sqli.model.ListingFilter;
import blind2.sqli.service.ListingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;

@Controller
public class PropertyListingController {

    private final ListingService listings;

    public PropertyListingController(ListingService listings) {
        this.listings = listings;
    }

    @GetMapping("/properties")
    public String list(@ModelAttribute ListingFilter filter, Model model) {
        model.addAttribute("results", listings.search(filter));
        model.addAttribute("filter", filter);
        return "properties/list";
    }
}
