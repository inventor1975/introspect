class CommentModerationController < ApplicationController
  def index
    author = params[:author]
    flagged = Comment.where("flagged = true AND author_name = '#{author}'")
    render json: flagged
  end
end
