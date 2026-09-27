package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.jsoup.Jsoup;
import org.jsoup.safety.Safelist;

@WebServlet("/profile/bio")
public class ProfileBioServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String bio = request.getParameter("bio");
        String cleaned = Jsoup.clean(bio == null ? "" : bio, Safelist.basic());
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<section class=\"bio\">" + cleaned + "</section>");
        out.println("<p class=\"hint\">Basic formatting (bold, italics, links) is kept.</p>");
    }
}
