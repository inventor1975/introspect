package blind2.xss.spring;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class DownloadPageController {

    @GetMapping("/downloads/ready")
    public void ready(@RequestParam("file") String file, HttpServletResponse response) throws IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter writer = response.getWriter();
        writer.write("<html><body><p>Your download <b>");
        writer.write(file);
        writer.write("</b> is ready.</p>");
        writer.write("<a href=\"/downloads/fetch\">Download now</a></body></html>");
        writer.flush();
    }
}
