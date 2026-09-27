class DefaultDashboardController < ApplicationController
  def index
    region = ENV.fetch("DEFAULT_REGION", "us")
    @widgets = Widget.find_by_sql(
      "SELECT * FROM widgets WHERE region = '#{region}' ORDER BY position"
    )
    render :index
  end
end
