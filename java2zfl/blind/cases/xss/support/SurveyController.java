package blind.xss.support;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SurveyController {

    @PostMapping("/support/survey/review")
    public ResponseEntity<String> review(@RequestParam("answer") List<String> answers) {
        StringBuilder sb = new StringBuilder("<h3>Please review your answers</h3><ol class=\"answers\">");
        for (int i = 0; i < answers.size(); i++) {
            String answer = answers.get(i);
            if (answer == null || answer.isBlank()) {
                continue;
            }
            sb.append("<li data-question=\"").append(i + 1).append("\">").append(answer).append("</li>");
        }
        sb.append("</ol>");
        return ResponseEntity.status(HttpStatus.OK)
                .header("Content-Type", "text/html;charset=UTF-8")
                .body(sb.toString());
    }
}
