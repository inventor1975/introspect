class FolderListingController < ApplicationController
  ROOT = "/srv/team_folders".freeze

  def show
    file_name = File.basename(params[:file].to_s)
    path = File.join(ROOT, params[:folder].to_s, file_name)

    if File.file?(path)
      send_file path
    else
      head :not_found
    end
  end
end
