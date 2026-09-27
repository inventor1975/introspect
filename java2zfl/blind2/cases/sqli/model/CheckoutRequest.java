package blind2.sqli.model;

public class CheckoutRequest {

    private long cartId;
    private int shippingOptionId;
    private String couponCode;
    private String customerNote;

    public long getCartId() {
        return cartId;
    }

    public void setCartId(long cartId) {
        this.cartId = cartId;
    }

    public int getShippingOptionId() {
        return shippingOptionId;
    }

    public void setShippingOptionId(int shippingOptionId) {
        this.shippingOptionId = shippingOptionId;
    }

    public String getCouponCode() {
        return couponCode;
    }

    public void setCouponCode(String couponCode) {
        this.couponCode = couponCode;
    }

    public String getCustomerNote() {
        return customerNote;
    }

    public void setCustomerNote(String customerNote) {
        this.customerNote = customerNote;
    }
}
