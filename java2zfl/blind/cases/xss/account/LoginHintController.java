package blind.xss.account;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class LoginHintController {

    @GetMapping(value = "/login/hint", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public String hint(@RequestParam(value = "code", defaultValue = "") String code) {
        String message = switch (code) {
            case "locked" -> "Your account is locked. Please contact support.";
            case "expired" -> "Your password has expired. Choose a new one to continue.";
            case "mfa" -> "Enter the six-digit code from your authenticator app.";
            default -> "Please sign in to continue.";
        };
        return "<p class=\"hint\">" + message + "</p>";
    }
}
