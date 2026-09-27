package blind2.sqli.support;

import java.util.Map;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;

public abstract class AbstractSortableServlet extends HttpServlet {

    protected abstract Map<String, String> sortColumns();

    protected abstract String defaultSort();

    protected String orderBy(HttpServletRequest request) {
        String requested = request.getParameter("sort");
        String column = requested == null ? null : sortColumns().get(requested);
        if (column == null) {
            column = defaultSort();
        }
        String dir = "desc".equalsIgnoreCase(request.getParameter("dir")) ? " DESC" : " ASC";
        return " ORDER BY " + column + dir;
    }
}
