package blind.sqli.support;

import javax.servlet.http.HttpServletRequest;

/** Invoked by the web filter chain before each request is dispatched. */
public final class ContextBinder {

    private ContextBinder() {
    }

    public static void bind(HttpServletRequest request) {
        String forwardedUser = request.getHeader("X-Forwarded-User");
        RequestContext.setUserName(forwardedUser != null ? forwardedUser : "anonymous");
    }
}
