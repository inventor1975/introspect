package blind2.sqli;

import blind2.sqli.model.CheckoutRequest;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CheckoutController {

    private final JdbcTemplate jdbc;

    public CheckoutController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/checkout")
    public ResponseEntity<Map<String, Object>> checkout(@RequestBody CheckoutRequest request) {
        int updated = jdbc.update(
                "UPDATE carts SET shipping_option_id = " + request.getShippingOptionId()
                        + ", coupon_code = ?, customer_note = ?, state = 'CHECKOUT' WHERE id = " + request.getCartId()
                        + " AND state = 'OPEN'",
                request.getCouponCode(), request.getCustomerNote());
        if (updated == 0) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return ResponseEntity.ok(Map.of("cartId", request.getCartId(), "state", "CHECKOUT"));
    }
}
