package blind.xss.reports;

/** For columns whose content is already rendered markup (rich-text notes, links built by the exporter). */
public class PlainCellFormatter implements CellFormatter {
    @Override
    public String format(String raw) {
        return raw == null ? "" : raw;
    }
}
