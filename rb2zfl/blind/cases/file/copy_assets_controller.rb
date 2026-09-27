require "fileutils"

class CopyAssetsController < ApplicationController
  TEMPLATES = Rails.root.join("site_templates").to_s
  SITE_DIR  = Rails.root.join("public", "sites").to_s

  def create
    src  = File.join(TEMPLATES, params[:source])
    dest = File.join(SITE_DIR, params[:dest])
    FileUtils.mkdir_p(File.dirname(dest))
    FileUtils.cp(src, dest)
    render json: { copied: params[:dest] }, status: :created
  end
end
