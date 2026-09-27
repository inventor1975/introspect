class TagBrowserController < ApplicationController
  def index
    tag = params[:tag]
    @posts = Post.where("tags @> ARRAY['#{tag}']::varchar[]")
    render :index
  end
end
