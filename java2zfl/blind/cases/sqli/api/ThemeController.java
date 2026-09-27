package blind.sqli.api;

import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ThemeController {

    private static final String PREFS_TABLE = "user_prefs";
    private final JdbcTemplate jdbc;

    public ThemeController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PutMapping("/api/v2/users/{userId}/theme")
    public ResponseEntity<Void> saveTheme(@PathVariable long userId,
                                          @CookieValue(name = "ui_theme", defaultValue = "light") String theme) {
        int updated = jdbc.update("UPDATE " + PREFS_TABLE + " SET theme = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = "
                + userId, theme);
        return updated == 1 ? ResponseEntity.ok().build() : ResponseEntity.badRequest().build();
    }
}
