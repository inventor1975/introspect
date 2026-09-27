class BillingSummaryController < ApplicationController
  def show
    account_id = params[:account_id].to_i
    @rows = ActiveRecord::Base.connection.select_all(
      "SELECT month, total FROM invoices WHERE account_id = #{account_id}"
    ).to_a
    render json: @rows
  end
end
