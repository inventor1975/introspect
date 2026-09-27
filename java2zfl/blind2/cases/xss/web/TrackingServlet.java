package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.UUID;

@WebServlet("/track")
public class TrackingServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String parcel = request.getParameter("parcel");
        UUID id;
        try {
            id = UUID.fromString(parcel);
        } catch (IllegalArgumentException | NullPointerException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid tracking id");
            return;
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Parcel " + id + "</h2>");
        out.println("<div id=\"map\" data-parcel=\"" + id.toString() + "\"></div></body></html>");
    }
}
