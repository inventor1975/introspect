package blind2.xss.spring;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class InvoiceController {

    @GetMapping("/invoices/{number}/header")
    @ResponseBody
    public String header(@PathVariable("number") Long number,
                         @RequestParam(value = "copy", defaultValue = "false") boolean copy) {
        String title = "Invoice " + number;
        if (copy) {
            title = title + " (copy)";
        }
        return "<header class=\"invoice\"><h1>" + title + "</h1><a href=\"/invoices/" + number + ".pdf\">PDF</a></header>";
    }
}
