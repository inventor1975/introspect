package blind2.sqli.model;

public enum ThreadSort {
    NEWEST("t.created_at DESC"),
    ACTIVE("t.last_post_at DESC"),
    POPULAR("t.reply_count DESC, t.last_post_at DESC");

    private final String orderBy;

    ThreadSort(String orderBy) {
        this.orderBy = orderBy;
    }

    public String orderBy() {
        return orderBy;
    }
}
