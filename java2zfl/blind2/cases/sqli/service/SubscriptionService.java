package blind2.sqli.service;

import blind2.sqli.data.SubscriptionDao;
import java.util.Locale;
import org.springframework.stereotype.Service;

@Service
public class SubscriptionService {

    private final SubscriptionDao dao;

    public SubscriptionService(SubscriptionDao dao) {
        this.dao = dao;
    }

    public boolean changePlan(long subscriptionId, String plan) {
        String planCode = plan.trim().toLowerCase(Locale.ROOT);
        return dao.updatePlan(subscriptionId, planCode) == 1;
    }
}
