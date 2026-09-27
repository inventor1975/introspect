package blind2.xss.support;

import org.springframework.web.util.HtmlUtils;

public class GuestEntry {
    private String name;
    private String message;
    private String city;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getDisplayName() {
        String n = (name == null || name.isBlank()) ? "Anonymous" : name.trim();
        if (city != null && !city.isBlank()) {
            n = n + " (" + city.trim() + ")";
        }
        return HtmlUtils.htmlEscape(n);
    }
}
