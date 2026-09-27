package blind.sqli.api;

public final class QueryBuilders {

    private QueryBuilders() {
    }

    public static String openOrders() {
        return "SELECT id, customer_id, total FROM orders WHERE status = 'OPEN' AND region = ?";
    }

    public static String lateShipments() {
        return "SELECT s.id, s.order_id FROM shipments s WHERE s.eta < CURRENT_DATE AND s.region = ?";
    }

    public static String refunds() {
        return "SELECT id, order_id, amount FROM refunds WHERE region = ? AND created_at > CURRENT_DATE - 30";
    }
}
