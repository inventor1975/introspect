class StatementsController < ApplicationController
  REPORTS = {
    "monthly"   => "monthly.csv",
    "quarterly" => "quarterly.csv",
    "yearly"    => "yearly.csv"
  }.freeze

  def show
    file = REPORTS[params[:period]]
    return head(:not_found) unless file

    send_file Rails.root.join("reports", file), type: "text/csv"
  end
end
