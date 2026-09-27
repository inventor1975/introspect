package blind2.sqli;

import blind2.sqli.model.SearchRequest;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ListingSearchController {

    public record ListingSummary(long id, String title, BigDecimal price) {
    }

    private final JdbcTemplate jdbc;

    public ListingSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/listings/search")
    public List<ListingSummary> search(@RequestBody SearchRequest request) {
        StringBuilder sql = new StringBuilder("SELECT id, title, price FROM listings WHERE status = 'ACTIVE'");
        List<Object> args = new ArrayList<>();
        if (request.getCity() != null) {
            sql.append(" AND city = ?");
            args.add(request.getCity());
        }
        if (request.getMaxPrice() != null) {
            sql.append(" AND price <= ?");
            args.add(request.getMaxPrice());
        }
        if (request.getKeyword() != null && !request.getKeyword().isBlank()) {
            sql.append(" AND title ILIKE '%").append(request.getKeyword().trim()).append("%'");
        }
        sql.append(" ORDER BY published_at DESC LIMIT 100");
        return jdbc.query(sql.toString(),
                (rs, rowNum) -> new ListingSummary(rs.getLong("id"), rs.getString("title"), rs.getBigDecimal("price")),
                args.toArray());
    }
}
