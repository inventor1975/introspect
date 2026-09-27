package blind.sqli.api;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QueryDispatchController {

    private final JdbcTemplate jdbc;

    public QueryDispatchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/ops/{report}")
    public ResponseEntity<List<Map<String, Object>>> run(@PathVariable String report,
                                                         @RequestParam String region) {
        String sql;
        try {
            Method m = QueryBuilders.class.getDeclaredMethod(report);
            if (!Modifier.isStatic(m.getModifiers()) || m.getReturnType() != String.class) {
                return ResponseEntity.badRequest().build();
            }
            sql = (String) m.invoke(null);
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(jdbc.queryForList(sql, region));
    }
}
