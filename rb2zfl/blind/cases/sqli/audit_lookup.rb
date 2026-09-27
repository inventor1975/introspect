class AuditController < ApplicationController
  def show
    actor = params[:actor]
    @events = AuditEvent.find_by_sql(
      "SELECT * FROM audit_events WHERE actor = '#{actor}' ORDER BY at DESC"
    )
    render :show
  end
end
