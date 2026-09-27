class WishlistController < ApplicationController
  def show
    @items = Wishlist.where(user_id: current_user.id)
                     .where("priority >= ?", params[:priority].to_i)
    render json: @items
  end
end
