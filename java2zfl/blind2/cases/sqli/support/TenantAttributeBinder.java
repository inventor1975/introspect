package blind2.sqli.support;

import java.util.Locale;
import javax.servlet.http.HttpServletRequest;

public final class TenantAttributeBinder {

    public static final String ATTRIBUTE = "tenant.code";

    private TenantAttributeBinder() {
    }

    public static void bind(HttpServletRequest request) {
        String tenant = request.getHeader("X-Tenant-Code");
        request.setAttribute(ATTRIBUTE, tenant == null ? "default" : tenant.toLowerCase(Locale.ROOT));
    }
}
