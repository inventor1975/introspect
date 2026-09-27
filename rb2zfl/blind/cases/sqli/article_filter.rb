class ArticlesController < ApplicationController
  def index
    category = params[:category]
    @articles = Article.where("category = '#{category}'").order(:published_at)
    render :index
  end
end
