package blind2.sqli.model;

public class ListingFilter {

    private String district;
    private Integer minRooms;
    private String sortBy;

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public Integer getMinRooms() {
        return minRooms;
    }

    public void setMinRooms(Integer minRooms) {
        this.minRooms = minRooms;
    }

    public String getSortBy() {
        return sortBy;
    }

    public void setSortBy(String sortBy) {
        this.sortBy = sortBy;
    }
}
