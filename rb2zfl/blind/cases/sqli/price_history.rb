class PriceHistoryController < ApplicationController
  def show
    sku = params[:sku]
    @history = ActiveRecord::Base.connection.exec_query(
      "SELECT recorded_on, price FROM price_history WHERE sku = ?",
      "price_history",
      [sku]
    ).to_a
    render json: @history
  end
end
