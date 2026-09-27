require_relative "lib/report_queries"

class VendorLedgerController < ApplicationController
  def index
    status = params[:status]
    fragment = ReportQueries.status_fragment(status)
    @entries = LedgerEntry.where(fragment)
    render json: @entries
  end
end
