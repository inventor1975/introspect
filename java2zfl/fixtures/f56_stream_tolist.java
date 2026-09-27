import org.springframework.web.bind.annotation.*;
import org.springframework.http.MediaType;
@RestController
public class F56 {
  @GetMapping(value = "/c", produces = MediaType.TEXT_HTML_VALUE)
  public String compare(@RequestParam("sku") java.util.List<String> skus) {
    java.util.List<String> cells = skus.stream().map(s -> "<th>" + s + "</th>").toList();
    return "<tr>" + String.join("", cells) + "</tr>";      // EXPECT: REFUTED (stream.toList() keeps the stream's taint)
  } }
