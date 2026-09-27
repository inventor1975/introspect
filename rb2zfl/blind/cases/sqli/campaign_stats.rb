class CampaignStatsController < ApplicationController
  def show
    name = params[:campaign]
    base = "SELECT clicks, opens FROM campaign_stats WHERE campaign = '"
    query = base + name + "'"
    @stats = Campaign.find_by_sql(query)
    render :show
  end
end
