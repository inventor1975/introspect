class AssetManagerController < ApplicationController
  def index
    column = case params[:group]
             when "type" then "asset_type"
             when "owner" then "owner_id"
             else "created_at"
             end
    @assets = Asset.order(column).group(column)
    render json: @assets.count
  end
end
