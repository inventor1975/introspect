package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

@Service
public class ProductSearchService {

    private static final int PAGE_SIZE = 20;
    private final JdbcTemplate jdbc;

    public ProductSearchService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Map<String, Object>> search(SearchRequest req) {
        StringBuilder sql = new StringBuilder("SELECT id, name, price FROM products WHERE active = TRUE");
        if (req.keyword() != null && !req.keyword().isBlank()) {
            sql.append(" AND LOWER(name) LIKE '%").append(req.keyword().toLowerCase()).append("%'");
        }
        if (req.category() != null) {
            sql.append(" AND category_id = ?");
            sql.append(" LIMIT ").append(PAGE_SIZE).append(" OFFSET ").append(Math.max(req.page(), 0) * PAGE_SIZE);
            return jdbc.queryForList(sql.toString(), req.category());
        }
        sql.append(" LIMIT ").append(PAGE_SIZE).append(" OFFSET ").append(Math.max(req.page(), 0) * PAGE_SIZE);
        return jdbc.queryForList(sql.toString());
    }
}
