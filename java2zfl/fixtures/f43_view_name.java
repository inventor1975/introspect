import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
@Controller
public class F43 {
  @GetMapping("/v")
  public String view(@RequestParam String q) { return "search"; }   // EXPECT: nothing (a view name, not a body)
}
