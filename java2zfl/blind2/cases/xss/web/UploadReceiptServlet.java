package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.UUID;
import javax.servlet.http.Part;

@WebServlet("/attachments/upload")
public class UploadReceiptServlet extends HttpServlet {

    private static final Path STORE = Path.of("/var/lib/helpdesk/attachments");

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Part part = request.getPart("file");
        if (part == null || part.getSize() == 0) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "No file");
            return;
        }
        String original = part.getSubmittedFileName();
        String storedName = UUID.randomUUID() + ".bin";
        try (InputStream in = part.getInputStream()) {
            Files.copy(in, STORE.resolve(storedName), StandardCopyOption.REPLACE_EXISTING);
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<p>Attached <strong>" + original + "</strong> (" + part.getSize() + " bytes).</p>");
        out.println("<a href=\"/tickets\">Back to ticket</a></body></html>");
    }
}
