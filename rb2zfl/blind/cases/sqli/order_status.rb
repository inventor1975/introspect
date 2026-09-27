class OrderStatusController < ApplicationController
  def index
    status = params[:status]
    @orders = Order.find_by_sql(
      ["SELECT * FROM orders WHERE status = ? ORDER BY placed_at DESC", status]
    )
    render json: @orders
  end
end
