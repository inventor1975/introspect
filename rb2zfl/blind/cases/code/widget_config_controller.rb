class DashboardWidgetsController < ApplicationController
  before_action :load_expression, only: [:evaluate]

  def evaluate
    metrics = Metric.for_account(current_account)
    value = metrics.instance_eval(@expression)
    render json: { value: value }
  end

  private

  def load_expression
    @expression = params[:widget][:expression]
  end
end
