package blind.xss.catalog;

/** Form backing object for the advanced product search. */
public class SearchForm {

    private String keyword;
    private String brand;
    private int maxPrice;
    private boolean inStockOnly;

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public int getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(int maxPrice) {
        this.maxPrice = maxPrice;
    }

    public boolean isInStockOnly() {
        return inStockOnly;
    }

    public void setInStockOnly(boolean inStockOnly) {
        this.inStockOnly = inStockOnly;
    }
}
