require_relative "lib/storage_paths"

class SharedFilesController < ApplicationController
  SHARED_ROOT = Rails.root.join("storage", "shared").to_s

  def show
    path = StoragePaths.resolve!(SHARED_ROOT, params[:path])
    send_file path
  rescue StoragePaths::OutsideRoot
    head :forbidden
  end
end
