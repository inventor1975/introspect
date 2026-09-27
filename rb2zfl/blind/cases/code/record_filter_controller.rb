class ProductSearchController < ApplicationController
  def index
    products = Product.limit(500).to_a
    field = params[:field] || "price"
    cmp = params[:cmp] || ">"
    value = params[:value] || "0"

    matches = products.select do |product|
      eval("product.#{field} #{cmp} #{value}")
    end

    render json: matches
  end
end
