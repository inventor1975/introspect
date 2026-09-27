class IncidentTimelineController < ApplicationController
  before_action :capture_scope

  def capture_scope
    @severity = params[:severity]
  end

  def index
    @incidents = Incident.where("severity = '#{@severity}'").order(:opened_at)
    render :index
  end
end
