package blind2.sqli;

import blind2.sqli.data.PluginQueries;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/marketplace/plugin-stats")
public class PluginQueryServlet extends HttpServlet {

    private PluginQueries queries;

    @Override
    public void init() throws ServletException {
        queries = new PluginQueries(DataSources.lookup("jdbc/marketplace"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String metric = req.getParameter("metric");
        String pluginId = req.getParameter("plugin");
        if (metric == null || metric.isEmpty() || pluginId == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String methodName = "count" + Character.toUpperCase(metric.charAt(0)) + metric.substring(1);
        try {
            Method method = PluginQueries.class.getMethod(methodName, String.class);
            Object value = method.invoke(queries, pluginId);
            resp.setContentType("text/plain");
            resp.getWriter().print(value);
        } catch (NoSuchMethodException e) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND, "unknown metric");
        } catch (InvocationTargetException e) {
            throw new ServletException(e.getCause());
        } catch (IllegalAccessException e) {
            throw new ServletException(e);
        }
    }
}
