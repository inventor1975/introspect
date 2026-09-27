class ProductsController < ApplicationController
  def index
    sort = params[:sort] || "name"
    dir = params[:dir] || "asc"
    @products = Product.order("#{sort} #{dir}").limit(50)
    render json: @products
  end
end
