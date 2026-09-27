package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.Part;
import org.owasp.esapi.ESAPI;
import org.owasp.esapi.Encoder;

@WebServlet("/gallery/upload")
public class UploadSummaryServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        List<String> names = new ArrayList<>();
        long total = 0;
        for (Part part : request.getParts()) {
            if (part.getSubmittedFileName() != null) {
                names.add(part.getSubmittedFileName());
                total += part.getSize();
            }
        }
        Encoder enc = ESAPI.encoder();
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Upload complete</h2><ul>");
        for (String n : names) {
            out.println("<li>" + enc.encodeForHTML(n) + "</li>");
        }
        out.println("</ul><p>" + total + " bytes received.</p></body></html>");
    }
}
