class UserSearchController < ApplicationController
  def index
    term = params[:q]
    @users = User.where("name LIKE '%#{term}%' OR email LIKE '%#{term}%'")
    render :index
  end
end
