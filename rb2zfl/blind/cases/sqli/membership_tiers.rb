class MembershipTiersController < ApplicationController
  def index
    tier = params[:tier]
    @members = Member.where(tier: tier).where("joined_at > ?", 1.year.ago)
    render json: @members
  end
end
