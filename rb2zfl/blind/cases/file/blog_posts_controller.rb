class BlogPostsController < ApplicationController
  POSTS_DIR = Rails.root.join("content", "posts")

  def show
    slug = params[:slug].to_s.downcase.delete("^a-z0-9-")
    @markdown = File.read(POSTS_DIR.join("#{slug}.md"))
    @slug = slug
  rescue Errno::ENOENT
    raise ActionController::RoutingError, "Not Found"
  end
end
