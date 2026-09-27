class CampaignLandingController < ApplicationController
  def landing
    campaign = request.GET['utm_campaign'] || 'direct'
    headline = "Special offer from #{campaign.tr('_', ' ')}"
    render html: "<section class=\"hero\"><h2>#{headline}</h2></section>".html_safe
  end
end
