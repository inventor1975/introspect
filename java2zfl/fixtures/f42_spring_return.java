import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
@RestController
public class F42 {
  @GetMapping(value = "/a", produces = MediaType.TEXT_HTML_VALUE)
  public String html(@RequestParam String q) { return "<h1>" + q + "</h1>"; }          // EXPECT: REFUTED (declared HTML)
  @GetMapping("/b")
  public String undeclared(@RequestParam String q) { return "hi " + q; }              // EXPECT: OPEN (the browser's Accept decides)
  @GetMapping(value = "/c", produces = MediaType.APPLICATION_JSON_VALUE)
  public String json(@RequestParam String q) { return "{\"q\":\"" + q + "\"}"; }      // EXPECT: nothing (not HTML)
  @GetMapping("/d")
  public ResponseEntity<String> entity(@RequestParam String q) {
    return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body("<p>" + q + "</p>"); }   // EXPECT: REFUTED
  @GetMapping("/e")
  public String unknownValue() { return helperLib.render(); }                           // EXPECT: nothing (unknown into a maybe-sink)
}
