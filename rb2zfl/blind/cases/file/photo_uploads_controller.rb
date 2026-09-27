require "securerandom"

class PhotoUploadsController < ApplicationController
  PHOTO_DIR = Rails.root.join("storage", "photos")
  ALLOWED_EXT = %w[.jpg .jpeg .png .webp].freeze

  def create
    upload = params.require(:photo)
    ext = File.extname(upload.original_filename.to_s).downcase
    return head(:unprocessable_entity) unless ALLOWED_EXT.include?(ext)

    name = "#{SecureRandom.uuid}#{ext}"
    File.binwrite(PHOTO_DIR.join(name), upload.read)
    Photo.create!(user: current_user, file_name: name, original_name: upload.original_filename)
    head :created
  end
end
