package blind.xss.reports;

/** Turns a raw cell value into the HTML that goes inside a table cell. */
public interface CellFormatter {
    String format(String raw);
}
