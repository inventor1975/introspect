class EventCalendarController < ApplicationController
  def index
    year = Integer(params[:year])
    month = Integer(params[:month])
    @events = Event.find_by_sql(
      "SELECT * FROM events WHERE YEAR(starts_at) = #{year} AND MONTH(starts_at) = #{month}"
    )
    render :index
  end
end
