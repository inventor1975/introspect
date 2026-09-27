class LoyaltyController < ApplicationController
  def leaderboard
    threshold = params[:min_points]
    @members = Member.where("points > #{threshold}")
                     .order(params[:sort] + " DESC")
    render :leaderboard
  end
end
