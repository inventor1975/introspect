class BlogPostsController < ApplicationController
  def index
    slug = params[:slug]
    @posts = Post.where("slug = :slug AND published = :p", slug: slug, p: true)
    render :index
  end
end
