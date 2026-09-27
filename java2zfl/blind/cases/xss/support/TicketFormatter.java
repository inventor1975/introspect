package blind.xss.support;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

/**
 * Renders entries of a ticket's activity log. Callers pass fragments that are already safe to embed.
 */
public class TicketFormatter {

    private final DateTimeFormatter dateFormat = DateTimeFormatter.ISO_LOCAL_DATE;

    public String line(String who, String what) {
        return "<li class=\"activity\"><span class=\"who\">" + who + "</span> " + what + "</li>";
    }

    public String datedLine(LocalDate date, String who, String what) {
        return "<li class=\"activity\"><time>" + dateFormat.format(date) + "</time> "
                + "<span class=\"who\">" + who + "</span> " + what + "</li>";
    }
}
