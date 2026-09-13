import org.springframework.web.bind.annotation.*;
@RestController
public class F9 {
  @GetMapping("/run")
  public void run(@RequestParam String cmd, @AuthenticationPrincipal String user) throws Exception {
    Runtime.getRuntime().exec(cmd);      // EXPECT: REFUTED [shell] (@RequestParam source)
    Runtime.getRuntime().exec(user);     // EXPECT: nothing (@AuthenticationPrincipal is not a request source)
  }
}
