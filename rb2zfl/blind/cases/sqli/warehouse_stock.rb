class WarehouseStockController < ApplicationController
  def index
    cols = params[:columns] || "sku, qty"
    @stock = Stock.select(cols).where(location: "main")
    render json: @stock
  end
end
