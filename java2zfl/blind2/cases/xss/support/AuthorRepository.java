package blind2.xss.support;

import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class AuthorRepository {

    private final JdbcTemplate jdbc;

    public AuthorRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public String findBio(long authorId) {
        List<String> rows = jdbc.queryForList("SELECT bio FROM authors WHERE id = ?", String.class, authorId);
        return rows.isEmpty() ? "" : rows.get(0);
    }

    public String findDisplayName(long authorId) {
        return jdbc.queryForObject("SELECT display_name FROM authors WHERE id = ?", String.class, authorId);
    }
}
