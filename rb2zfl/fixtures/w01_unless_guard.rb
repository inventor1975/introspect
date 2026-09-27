class ReportsController < ApplicationController
  ALLOWED = %w[daily weekly].freeze
  def show
    period = params[:period]
    return head(:bad_request) unless ALLOWED.include?(period)
    File.read("reports/#{period}.csv")
    Report.find_by_sql("SELECT * FROM #{period}_reports")
  end
  def legacy
    kind = params[:kind]
    unless ALLOWED.include?(kind)
      Report.find_by_sql("SELECT * FROM logs WHERE kind = '#{kind}'") # the branch where the check FAILED
    end
  end
end
