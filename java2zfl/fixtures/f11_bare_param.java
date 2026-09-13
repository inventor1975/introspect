import org.springframework.web.bind.annotation.*;
@RestController
public class F11 {
  @GetMapping("/x")
  public void x(String filepath) throws Exception {          // bare simple param: Spring auto-binds from request
    Runtime.getRuntime().exec("ls " + filepath);             // EXPECT: REFUTED [shell] (implicit @RequestParam)
  }
}
