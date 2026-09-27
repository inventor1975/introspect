require_relative "lib/expression_tools"

class AnalyticsExpressionsController < ApplicationController
  def show
    values = params[:values].to_s.split(",").map(&:to_f)
    info = ExpressionTools.describe(params[:expression])
    average = ExpressionTools.evaluate(ExpressionTools::DEFAULT_EXPRESSION, values)
    render json: { requested: info, average: average }
  end
end
