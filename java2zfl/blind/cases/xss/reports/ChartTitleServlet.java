package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/reports/revenue-chart")
public class ChartTitleServlet extends HttpServlet {

    private String chartTitle;

    @Override
    public void init() throws ServletException {
        chartTitle = getInitParameter("chart.title");
        if (chartTitle == null) {
            chartTitle = "Monthly revenue";
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String range = req.getParameter("range");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h2 class=\"chart-title\">" + chartTitle + "</h2>");
        out.println("<p class=\"range\">Range: " + Encode.forHtml(range == null ? "last 12 months" : range) + "</p>");
        out.println("<canvas id=\"revenue\"></canvas>");
    }
}
