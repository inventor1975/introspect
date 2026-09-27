class ReportsController < ApplicationController
  def index
    scope = case params[:sort]
            when "name" then :by_name
            when "amount" then :by_amount
            when "oldest" then :oldest_first
            else :newest_first
            end
    @reports = Report.public_send(scope).page(params[:page])
  end
end
