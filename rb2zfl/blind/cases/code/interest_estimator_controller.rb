class InterestEstimatorController < ApplicationController
  BASE_EXPRESSION = "principal * (1 + rate / 100.0) ** years".freeze

  def estimate
    principal = params[:principal].to_f
    rate = params[:rate].to_f
    years = params[:years].to_i.clamp(0, 50)
    total = eval(BASE_EXPRESSION, binding)
    render json: { total: total.round(2) }
  end
end
