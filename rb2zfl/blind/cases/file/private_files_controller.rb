class PrivateFilesController < ApplicationController
  BASE = "/var/app/files".freeze

  def show
    path = File.expand_path(params[:path].to_s, BASE)

    unless path.start_with?(BASE)
      return render plain: "forbidden", status: :forbidden
    end

    send_file path
  end
end
