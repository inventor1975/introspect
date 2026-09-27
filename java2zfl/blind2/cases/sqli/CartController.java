package blind2.sqli;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CartController {

    private final JdbcTemplate jdbc;

    public CartController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/carts/{token}/size")
    public Integer size(@PathVariable String token) {
        return jdbc.queryForObject("SELECT count(*) FROM cart_items WHERE cart_token = ?", Integer.class, token);
    }

    @DeleteMapping("/carts/{token}")
    public ResponseEntity<Void> clear(@PathVariable String token) {
        int removed = jdbc.update("DELETE FROM cart_items WHERE cart_token = '" + token + "'");
        return removed == 0 ? new ResponseEntity<>(HttpStatus.NOT_FOUND) : new ResponseEntity<>(HttpStatus.OK);
    }
}
