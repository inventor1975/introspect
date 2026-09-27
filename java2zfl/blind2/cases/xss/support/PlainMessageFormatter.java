package blind2.xss.support;

/** Used by the CLI export and unit tests, where no HTML is produced. */
public class PlainMessageFormatter implements MessageFormatter {
    @Override
    public String format(String template, String subject) {
        return template.replace("{}", subject == null ? "" : subject);
    }
}
