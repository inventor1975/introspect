class AvatarCropsController < ApplicationController
  before_action :authenticate_user!

  def update
    image = params.require(:image)
    path = Rails.root.join("storage", "avatars", "#{current_user.id}.png")
    File.binwrite(path, image.read)
    redirect_to profile_path(crop: params[:crop]), notice: "Avatar updated"
  end
end
