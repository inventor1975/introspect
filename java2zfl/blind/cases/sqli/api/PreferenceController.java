package blind.sqli.api;

import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PreferenceController {

    private final JdbcTemplate jdbc;

    public PreferenceController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PutMapping("/api/users/{userId}/theme")
    public ResponseEntity<Void> saveTheme(@PathVariable long userId,
                                          @CookieValue(name = "ui_theme", defaultValue = "light") String theme) {
        int updated = jdbc.update("UPDATE user_prefs SET theme = '" + theme + "' WHERE user_id = ?", userId);
        return updated == 1 ? ResponseEntity.ok().build() : ResponseEntity.badRequest().build();
    }
}
