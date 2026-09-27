class SalesDashboardController < ApplicationController
  def summary
    quarter = params[:quarter]
    totals = ActiveRecord::Base.connection.select_all(
      "SELECT region, SUM(amount) AS total FROM sales " \
      "WHERE quarter = '#{quarter}' GROUP BY region"
    )
    render json: totals.to_a
  end
end
