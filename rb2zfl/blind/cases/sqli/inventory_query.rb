class InventoryController < ApplicationController
  def lookup
    warehouse = params[:warehouse]
    result = ActiveRecord::Base.connection.execute(
      "SELECT sku, qty FROM stock WHERE warehouse = '#{warehouse}'"
    )
    render json: result.to_a
  end
end
