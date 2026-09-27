package blind.xss.support;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SurveyResultController {

    @PostMapping("/support/survey/score")
    public ResponseEntity<String> score(@RequestParam("answer") List<String> answers) {
        int total = 0;
        int counted = 0;
        for (String answer : answers) {
            try {
                int value = Integer.parseInt(answer.trim());
                if (value < 1 || value > 10) {
                    continue;
                }
                total += value;
                counted++;
            } catch (NumberFormatException e) {
                // free-text answers are not scored
            }
        }
        double average = counted == 0 ? 0.0 : (double) total / counted;
        String html = String.format("<p>Thanks! Your average rating was <b>%.1f</b> across %d answers.</p>", average, counted);
        return ResponseEntity.status(HttpStatus.OK)
                .header("Content-Type", "text/html;charset=UTF-8")
                .body(html);
    }
}
