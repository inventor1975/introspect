package blind.sqli.api;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DocumentSearchController {

    private final DataSource dataSource;

    public DocumentSearchController(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @GetMapping("/api/v2/documents")
    public List<String> documents(@RequestParam String title,
                                  @RequestHeader("X-User") String owner,
                                  @RequestParam(defaultValue = "50") int limit) throws SQLException {
        String sql = "SELECT id, title FROM documents WHERE owner = ? AND title LIKE ? ESCAPE '!'"
                + " AND deleted = ? ORDER BY updated_at DESC LIMIT ?";
        String pattern = "%" + title.replace("!", "!!").replace("%", "!%").replace("_", "!_") + "%";
        List<String> titles = new ArrayList<>();
        try (Connection conn = dataSource.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, owner);
            ps.setString(2, pattern);
            ps.setBoolean(3, false);
            ps.setInt(4, Math.min(limit, 200));
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    titles.add(rs.getString("title"));
                }
            }
        }
        return titles;
    }
}
