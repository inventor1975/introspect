package blind2.xss.support;

public class PassThroughRenderer implements Renderer {
    @Override
    public String render(String text) {
        return text == null ? "" : text;
    }
}
