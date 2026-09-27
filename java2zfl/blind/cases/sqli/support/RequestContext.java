package blind.sqli.support;

public final class RequestContext {

    private static final ThreadLocal<String> USER_NAME = new ThreadLocal<>();

    private RequestContext() {
    }

    public static void setUserName(String name) {
        USER_NAME.set(name);
    }

    public static String userName() {
        return USER_NAME.get();
    }

    public static void clear() {
        USER_NAME.remove();
    }
}
