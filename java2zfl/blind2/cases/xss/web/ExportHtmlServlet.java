package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;

@WebServlet("/export/table")
public class ExportHtmlServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String caption = request.getParameter("caption");
        String[] cols = {"Date", "Amount", "Status"};
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter pw = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(response.getOutputStream(), StandardCharsets.UTF_8)))) {
            pw.append("<table><caption>").append(caption == null ? "Export" : caption).append("</caption><tr>");
            for (String c : cols) {
                pw.append("<th>").append(c).append("</th>");
            }
            pw.append("</tr></table>");
        }
    }
}
