class ReportsController < ApplicationController
  def export
    from = params[:from]
    to = params[:to]
    sql = "SELECT * FROM orders WHERE created_at BETWEEN '#{from}' AND '#{to}'"
    @rows = ActiveRecord::Base.connection.select_all(sql)
    send_data @rows.to_csv, filename: "orders.csv"
  end
end
