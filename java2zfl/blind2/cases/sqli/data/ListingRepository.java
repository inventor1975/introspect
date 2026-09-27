package blind2.sqli.data;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class ListingRepository {

    private final NamedParameterJdbcTemplate named;

    public ListingRepository(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    public List<Map<String, Object>> find(String district, int minRooms, String sortColumn) {
        String sql = "SELECT id, address, rooms, price FROM properties"
                + " WHERE district = :district AND rooms >= :rooms"
                + " ORDER BY " + sortColumn;
        Map<String, Object> params = new HashMap<>();
        params.put("district", district);
        params.put("rooms", minRooms);
        return named.queryForList(sql, params);
    }
}
