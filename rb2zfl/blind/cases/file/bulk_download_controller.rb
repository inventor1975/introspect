class BulkDownloadController < ApplicationController
  SHARE_DIR = "/srv/share/public".freeze

  def create
    names = Array(params[:files]).map(&:to_s).reject(&:empty?)
    contents = {}

    names.each do |n|
      contents[n] = File.read(File.join(SHARE_DIR, n))
    end

    render json: contents
  end
end
