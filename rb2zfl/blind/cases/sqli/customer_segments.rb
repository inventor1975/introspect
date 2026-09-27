class CustomerSegmentsController < ApplicationController
  def index
    tier = params[:tier]
    region = params[:region]
    @customers = Customer.where(
      "tier = '#{tier}' AND region = '#{region}'"
    ).limit(100)
    render json: @customers
  end
end
