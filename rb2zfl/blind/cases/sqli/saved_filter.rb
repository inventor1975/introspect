class SavedFilterController < ApplicationController
  def index
    fragment = Setting.find_by(key: "reports.default_filter")&.value || "1=1"
    @reports = Report.where(fragment).order(:generated_at)
    render json: @reports
  end
end
