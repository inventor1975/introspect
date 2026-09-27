require_relative "lib/query_guards"

class LeaderboardController < ApplicationController
  def index
    sort = QueryGuards.safe_sort(params[:sort], "score")
    dir = QueryGuards.safe_direction(params[:dir])
    @players = Player.order("#{sort} #{dir}").limit(20)
    render json: @players
  end
end
