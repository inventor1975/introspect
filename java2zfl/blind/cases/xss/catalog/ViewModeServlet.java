package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/view")
public class ViewModeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String mode = req.getParameter("mode");
        if (mode == null) {
            mode = "grid";
        }
        String cssClass;
        String label;
        switch (mode) {
            case "grid":
                cssClass = "view-grid";
                label = "Grid";
                break;
            case "list":
                cssClass = "view-list";
                label = "List";
                break;
            case "compact":
                cssClass = "view-compact";
                label = "Compact";
                break;
            default:
                cssClass = "view-grid";
                label = mode;
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.printf("<div class=\"%s\"><span class=\"mode\">Viewing as: %s</span></div>%n", cssClass, label);
    }
}
