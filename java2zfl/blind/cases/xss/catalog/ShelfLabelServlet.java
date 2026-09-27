package blind.xss.catalog;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/shelf-label")
public class ShelfLabelServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String label = req.getParameter("label");
        String aisle = req.getParameter("aisle");
        String html = "<div class=\"shelf-label\"><span class=\"aisle\">Aisle " + (aisle == null ? "?" : aisle.length())
                + "</span><span class=\"text\">" + label + "</span></div>";
        resp.setContentType("text/html; charset=UTF-8");
        ServletOutputStream os = resp.getOutputStream();
        os.write(html.getBytes(StandardCharsets.UTF_8));
        os.flush();
    }
}
