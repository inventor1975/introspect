package blind2.sqli.support;

public final class SqlFragments {

    private SqlFragments() {
    }

    public static String like(String column, String value) {
        return column + " LIKE '%" + value + "%'";
    }

    public static String eq(String column, long value) {
        return column + " = " + value;
    }

    public static String and(String... conditions) {
        return String.join(" AND ", conditions);
    }
}
