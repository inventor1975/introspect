class TeamMembersController < ApplicationController
  def index
    role = params[:role]
    @members = TeamMember.where(role: role)
                         .includes(:profile)
                         .order(:joined_on)
    render json: @members
  end
end
