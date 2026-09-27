class DownloadsController < ApplicationController
  def show
    send_file params[:file]
  end
  def purge
    FileUtils.rm_rf(File.join("/srv/tmp", params[:dir]))
  end
end
