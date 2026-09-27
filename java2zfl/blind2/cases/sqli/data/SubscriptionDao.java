package blind2.sqli.data;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class SubscriptionDao {

    private final JdbcTemplate jdbc;

    public SubscriptionDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public int updatePlan(long subscriptionId, String planCode) {
        return jdbc.update("UPDATE subscriptions SET plan_code = '" + planCode + "', changed_at = now() WHERE id = " + subscriptionId);
    }

    public Integer seatsFor(long subscriptionId) {
        return jdbc.queryForObject("SELECT seats FROM subscriptions WHERE id = ?", Integer.class, subscriptionId);
    }
}
