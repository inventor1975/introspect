class RegionSelectorController < ApplicationController
  VALID_REGIONS = %w[us eu apac latam].freeze

  def index
    region = params[:region]
    return head(:bad_request) unless VALID_REGIONS.include?(region)

    @stores = Store.find_by_sql("SELECT * FROM stores WHERE region = '#{region}'")
    render json: @stores
  end
end
