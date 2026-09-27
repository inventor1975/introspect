package blind2.xss.support;

import java.io.IOException;
import java.io.Writer;
import org.owasp.encoder.Encode;

/** Small writers shared by the newsletter pages. */
public final class HtmlFragments {

    private HtmlFragments() {
    }

    public static void paragraph(Writer out, String html) throws IOException {
        out.write("<p class=\"nl-body\">");
        out.write(html);
        out.write("</p>\n");
    }

    public static void textParagraph(Writer out, String text) throws IOException {
        out.write("<p class=\"nl-body\">");
        out.write(Encode.forHtmlContent(text));
        out.write("</p>\n");
    }

    public static void heading(Writer out, String title) throws IOException {
        out.write("<h2>");
        out.write(Encode.forHtml(title));
        out.write("</h2>\n");
    }
}
