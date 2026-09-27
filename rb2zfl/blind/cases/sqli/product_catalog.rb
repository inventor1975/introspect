class ProductCatalogController < ApplicationController
  def index
    @products = Product.where(category: params[:category], active: true)
                       .order(:name)
                       .limit(50)
    render json: @products
  end
end
