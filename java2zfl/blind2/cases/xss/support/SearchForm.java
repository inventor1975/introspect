package blind2.xss.support;

public class SearchForm {
    private String query;
    private String category;
    private int page = 1;

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public int getPage() { return page; }
    public void setPage(int page) { this.page = page; }
}
