class LineItemTotalsController < ApplicationController
  def show
    expression = format("%d * %d", params[:quantity], params[:unit_cents])
    total_cents = eval(expression)
    render json: { total_cents: total_cents }
  rescue ArgumentError, TypeError
    render json: { error: "quantity and unit_cents must be integers" }, status: :bad_request
  end
end
