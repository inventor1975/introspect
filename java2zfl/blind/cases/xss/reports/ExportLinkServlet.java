package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.util.UriUtils;

@WebServlet("/reports/export-button")
public class ExportLinkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String report = req.getParameter("report");
        if (report == null) {
            report = "monthly";
        }
        String encoded = UriUtils.encodeQueryParam(report, "UTF-8");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<button type=\"button\" class=\"export\" "
                + "onclick=\"downloadReport('/reports/export?name=" + encoded + "&format=csv')\">Download CSV</button>");
    }
}
