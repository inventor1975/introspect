package blind2.xss.spring;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.time.format.TextStyle;
import java.util.Locale;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CalendarController {

    @GetMapping("/calendar/day")
    public ResponseEntity<String> day(@RequestParam("date") String date) {
        LocalDate day;
        try {
            day = LocalDate.parse(date);
        } catch (DateTimeParseException e) {
            return ResponseEntity.badRequest().body("<p class=\"error\">Please use the format YYYY-MM-DD.</p>");
        }
        DayOfWeek dow = day.getDayOfWeek();
        return ResponseEntity.ok("<h2>" + dow.getDisplayName(TextStyle.FULL, Locale.ENGLISH) + ", " + day + "</h2>"
                + "<div id=\"agenda\" data-day=\"" + day + "\"></div>");
    }
}
