require_relative "lib/report_queries"

class InventoryReportController < ApplicationController
  def index
    condition = ReportQueries.status_binding(params[:status])
    @items = InventoryItem.where(condition)
    render json: @items
  end
end
