import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
@RestController
public class F52 {
  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<String> bad(IllegalArgumentException ex) {
    return ResponseEntity.status(400).contentType(MediaType.TEXT_HTML).body("<p>" + ex.getMessage() + "</p>");  // EXPECT: OPEN
  } }
