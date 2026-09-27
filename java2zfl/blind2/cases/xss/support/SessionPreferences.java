package blind2.xss.support;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

/** Called from the account settings form handler. */
public final class SessionPreferences {

    private SessionPreferences() {
    }

    public static void remember(HttpServletRequest request) {
        HttpSession session = request.getSession();
        String displayName = request.getParameter("displayName");
        if (displayName != null) {
            session.setAttribute("displayName", displayName.trim());
        }
        String tz = request.getParameter("tz");
        if (tz != null) {
            session.setAttribute("tz", tz);
        }
    }
}
