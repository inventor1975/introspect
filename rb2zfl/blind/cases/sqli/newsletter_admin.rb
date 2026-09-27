class NewsletterAdminController < ApplicationController
  DIRECTIONS = { "new" => "created_at DESC", "old" => "created_at ASC" }.freeze

  def index
    ordering = DIRECTIONS.fetch(params[:order], "created_at DESC")
    @subscribers = Subscriber.order(ordering)
    render json: @subscribers
  end
end
