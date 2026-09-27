class CouponRedeemController < ApplicationController
  def show
    code = params[:code]
    quoted = ActiveRecord::Base.connection.quote(code)
    @coupon = Coupon.find_by_sql(
      "SELECT * FROM coupons WHERE code = #{quoted} AND redeemed = false"
    ).first
    render json: @coupon
  end
end
