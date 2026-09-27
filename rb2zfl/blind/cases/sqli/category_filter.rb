class CategoryFilterController < ApplicationController
  def index
    @items = Item.where("price BETWEEN ? AND ?", params[:min], params[:max])
                 .where(category: params[:category])
    render json: @items
  end
end
