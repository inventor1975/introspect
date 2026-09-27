package blind2.xss.spring;

import javax.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class WizardController {

    @PostMapping("/onboarding/step1")
    public String step1(@RequestParam("company") String company, HttpSession session) {
        session.setAttribute("wizard.company", company);
        return "redirect:/onboarding/step2";
    }

    @GetMapping(value = "/onboarding/step2", produces = "text/html")
    @ResponseBody
    public String step2(HttpSession session) {
        Object company = session.getAttribute("wizard.company");
        return "<h2>Step 2 of 3</h2><p>Let's set up billing for <b>" + company + "</b>.</p>";
    }
}
