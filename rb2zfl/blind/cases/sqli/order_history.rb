class OrderHistoryController < ApplicationController
  def index
    status = params[:status]
    @orders = current_user.orders.where("status = '#{status}'")
    render :index
  end
end
