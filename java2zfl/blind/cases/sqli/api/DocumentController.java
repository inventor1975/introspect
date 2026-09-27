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
public class DocumentController {

    private final DataSource dataSource;

    public DocumentController(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @GetMapping("/api/documents")
    public List<String> documents(@RequestParam String title,
                                  @RequestHeader("X-User") String owner,
                                  @RequestParam(defaultValue = "50") int limit) throws SQLException {
        String sql = "SELECT id, title FROM documents WHERE owner = ? AND title LIKE '%" + title
                + "%' AND deleted = ? ORDER BY updated_at DESC LIMIT ?";
        List<String> titles = new ArrayList<>();
        try (Connection conn = dataSource.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, owner);
            ps.setBoolean(2, false);
            ps.setInt(3, Math.min(limit, 200));
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    titles.add(rs.getString("title"));
                }
            }
        }
        return titles;
    }
}
