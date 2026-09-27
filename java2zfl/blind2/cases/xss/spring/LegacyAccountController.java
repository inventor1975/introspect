package blind2.xss.spring;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class LegacyAccountController {

    @GetMapping("/account/summary")
    public ModelAndView summary(@RequestParam(value = "nickname", required = false) String nickname,
                                @RequestParam(value = "tab", defaultValue = "overview") String tab) {
        ModelAndView mav = new ModelAndView("account/summary");
        mav.addObject("nickname", nickname == null ? "" : nickname);
        mav.addObject("tab", tab);
        return mav;
    }
}
