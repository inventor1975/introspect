package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.Markup;

@WebServlet("/mail/signature")
public class EmailSignatureServlet extends HttpServlet {

    /** Signatures are allowed to contain basic formatting. */
    private static final boolean ESCAPE_SIGNATURE = false;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String signature = request.getParameter("signature");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"sig-preview\">--<br>" + Markup.fragment(signature, ESCAPE_SIGNATURE) + "</div>");
    }
}
