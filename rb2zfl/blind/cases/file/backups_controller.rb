class BackupsController < ApplicationController
  BACKUP_ROOT = "/var/backups/app".freeze

  def fetch
    full = File.join(BACKUP_ROOT, params[:file].to_s)

    if full.start_with?(BACKUP_ROOT)
      send_file full, type: "application/gzip"
    else
      render plain: "forbidden", status: :forbidden
    end
  end
end
