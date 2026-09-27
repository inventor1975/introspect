package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StoreLocatorController {

    @GetMapping(value = "/stores/near/{city}", produces = MediaType.TEXT_HTML_VALUE)
    public String near(@PathVariable("city") String city,
                       @RequestParam(value = "zip", required = false) String zip) {
        String area = (zip != null && !zip.isBlank()) ? zip.trim() : city;
        StringBuilder sb = new StringBuilder("<h2>Stores near ");
        sb.append(area).append("</h2>");
        sb.append("<ul id=\"stores\" data-src=\"/api/stores\"></ul>");
        return sb.toString();
    }
}
