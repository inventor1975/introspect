require "fileutils"

class UserAvatarsController < ApplicationController
  AVATAR_DIR = Rails.root.join("public", "avatars")

  def destroy
    FileUtils.rm_f(AVATAR_DIR.join(params[:avatar_name]))
    current_user.update!(avatar_name: nil)
    redirect_to edit_profile_path, notice: "Avatar removed"
  end
end
