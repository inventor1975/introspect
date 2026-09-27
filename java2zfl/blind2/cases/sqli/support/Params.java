package blind2.sqli.support;

import javax.servlet.http.HttpServletRequest;

public final class Params {

    private Params() {
    }

    public static String text(HttpServletRequest request, String name, String fallback) {
        String value = request.getParameter(name);
        if (value == null) {
            return fallback;
        }
        value = value.trim();
        return value.isEmpty() ? fallback : value;
    }

    public static int integer(HttpServletRequest request, String name, int fallback) {
        String value = request.getParameter(name);
        if (value == null) {
            return fallback;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            return fallback;
        }
    }
}
