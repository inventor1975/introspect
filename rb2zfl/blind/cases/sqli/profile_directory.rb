class ProfileDirectoryController < ApplicationController
  def index
    handle = current_user.display_handle
    @matches = Profile.find_by_sql(
      "SELECT * FROM profiles WHERE referred_by = '#{handle}'"
    )
    render :index
  end
end
