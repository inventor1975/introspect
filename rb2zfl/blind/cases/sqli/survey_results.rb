class SurveyResultsController < ApplicationController
  ALLOWED_SORTS = %w[score submitted_at respondent].freeze

  def index
    sort = ALLOWED_SORTS.include?(params[:sort]) ? params[:sort] : "submitted_at"
    @results = SurveyResponse.order("#{sort} DESC").limit(100)
    render json: @results
  end
end
