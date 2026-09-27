class AnalyticsSummaryController < ApplicationController
  def index
    days = params[:days].to_i
    days = 30 if days <= 0
    @rows = ActiveRecord::Base.connection.select_all(
      "SELECT day, hits FROM analytics WHERE day > CURRENT_DATE - #{days}"
    ).to_a
    render json: @rows
  end
end
