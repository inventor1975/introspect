package blind.xss.account;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.util.HtmlUtils;

@Controller
public class LoginErrorController {

    @GetMapping("/login/error")
    @ResponseBody
    public String error(@RequestParam(value = "reason", defaultValue = "Invalid credentials") String reason,
                        @RequestParam(value = "username", required = false) String username) {
        String who = username == null ? "" : " for <b>" + HtmlUtils.htmlEscape(username) + "</b>";
        return String.format("<div class=\"alert alert-danger\">Sign-in failed%s: %s</div>", who, reason);
    }
}
