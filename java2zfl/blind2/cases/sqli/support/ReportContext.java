package blind2.sqli.support;

public final class ReportContext {

    private static final ThreadLocal<String> REGION = new ThreadLocal<>();

    private ReportContext() {
    }

    public static void setRegion(String region) {
        REGION.set(region);
    }

    public static String region() {
        return REGION.get();
    }

    public static void clear() {
        REGION.remove();
    }
}
