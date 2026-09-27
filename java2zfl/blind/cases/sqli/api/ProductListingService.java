package blind.sqli.api;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Service;

@Service
public class ProductListingService {

    private static final int PAGE_SIZE = 20;
    private final NamedParameterJdbcTemplate named;

    public ProductListingService(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    public List<Map<String, Object>> list(SearchRequest req) {
        Map<String, Object> params = new HashMap<>();
        StringBuilder sql = new StringBuilder("SELECT id, name, price FROM products WHERE active = TRUE");
        if (req.keyword() != null && !req.keyword().isBlank()) {
            sql.append(" AND LOWER(name) LIKE :kw");
            params.put("kw", "%" + req.keyword().toLowerCase() + "%");
        }
        if (req.category() != null) {
            sql.append(" AND category_id = :cat");
            params.put("cat", req.category());
        }
        sql.append(" LIMIT ").append(PAGE_SIZE).append(" OFFSET ").append(Math.max(req.page(), 0) * PAGE_SIZE);
        return named.queryForList(sql.toString(), params);
    }
}
