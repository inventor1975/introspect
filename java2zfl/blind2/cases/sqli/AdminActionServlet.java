package blind2.sqli;

import blind2.sqli.data.MaintenanceActions;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/maintenance")
public class AdminActionServlet extends HttpServlet {

    private static final Map<String, String> ACTIONS = Map.of(
            "purge-sessions", "purgeSessionsFor",
            "unlock", "unlockAccount");

    private MaintenanceActions actions;

    @Override
    public void init() throws ServletException {
        actions = new MaintenanceActions(DataSources.lookup("jdbc/auth"));
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String action = req.getParameter("action");
        String methodName = action == null ? null : ACTIONS.get(action);
        if (methodName == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "unknown action");
            return;
        }
        String login = req.getParameter("login");
        try {
            Method method = MaintenanceActions.class.getMethod(methodName, String.class);
            Object affected = method.invoke(actions, login);
            resp.setContentType("text/plain");
            resp.getWriter().println(action + ": " + affected);
        } catch (InvocationTargetException e) {
            throw new ServletException(e.getCause());
        } catch (ReflectiveOperationException e) {
            throw new ServletException(e);
        }
    }
}
