package blind.xss.account;

import java.util.Locale;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LanguageController {

    @GetMapping(value = "/account/language/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam(value = "lang", defaultValue = "en") String lang) {
        String tag = Locale.forLanguageTag(lang).toLanguageTag();
        return "<!DOCTYPE html><html lang=\"" + tag + "\"><head><meta charset=\"utf-8\"></head>"
                + "<body><p>Preview for locale <code>" + tag + "</code></p></body></html>";
    }
}
