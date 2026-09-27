package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.LinkedHashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

@WebServlet("/embed/widget")
public class WidgetBootstrapServlet extends HttpServlet {

    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("siteKey", request.getParameter("site"));
        config.put("placement", request.getParameter("placement"));
        config.put("version", 3);
        String json = mapper.writeValueAsString(config);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<!DOCTYPE html><html><head>");
        out.println("<script>window.__WIDGET__ = " + json + ";</script>");
        out.println("<script src=\"/static/widget.js\"></script></head><body></body></html>");
    }
}
