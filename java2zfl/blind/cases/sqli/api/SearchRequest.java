package blind.sqli.api;

public record SearchRequest(String keyword, String category, int page) {
}
