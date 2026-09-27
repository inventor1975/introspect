package blind2.xss.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.LayoutServlet;

@WebServlet("/dashboard/notice")
public class DashboardNoticeServlet extends LayoutServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String notice = request.getParameter("notice");
        String body = "<div class=\"notice\">" + (notice == null ? "Nothing new." : notice) + "</div>";
        writePage(response, "Notices", body);
    }
}
