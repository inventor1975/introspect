package blind2.xss.support;

import javax.servlet.http.HttpServletRequest;

/** Populated by the tenant filter at the start of every request. */
public final class TenantContext {

    private static final ThreadLocal<String> TENANT = new ThreadLocal<>();

    private TenantContext() {
    }

    public static void bind(HttpServletRequest request) {
        String tenant = request.getParameter("tenant");
        if (tenant == null) {
            tenant = request.getHeader("X-Tenant");
        }
        TENANT.set(tenant);
    }

    public static String currentTenant() {
        String t = TENANT.get();
        return t == null ? "default" : t;
    }

    public static void clear() {
        TENANT.remove();
    }
}
