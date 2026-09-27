class AttachmentsController < ApplicationController
  before_action :authenticate_user!

  def show
    path = Rails.root.join("storage", "attachments", params[:filename])
    if File.exist?(path)
      send_file path, disposition: "attachment"
    else
      head :not_found
    end
  end
end
