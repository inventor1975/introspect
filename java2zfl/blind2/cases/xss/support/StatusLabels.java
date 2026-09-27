package blind2.xss.support;

public final class StatusLabels {

    private StatusLabels() {
    }

    public static String label(String code) {
        if (code == null) {
            return "Unknown";
        }
        switch (code) {
            case "NEW":
                return "Received";
            case "PICK":
                return "Being packed";
            case "SHIP":
                return "On its way";
            case "DLV":
                return "Delivered";
            default:
                return "Unknown";
        }
    }

    public static String labelOrCode(String code) {
        if (code == null) {
            return "";
        }
        return switch (code) {
            case "OPEN" -> "Open";
            case "WAIT" -> "Waiting for customer";
            case "DONE" -> "Resolved";
            default -> code;
        };
    }
}
