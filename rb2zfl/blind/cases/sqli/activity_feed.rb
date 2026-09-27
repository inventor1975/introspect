class ActivityFeedController < ApplicationController
  def index
    kind = params[:kind]
    @events = Activity.where(kind: kind)
                      .where("occurred_at > ?", params[:since])
                      .order(occurred_at: :desc)
    render json: @events
  end
end
