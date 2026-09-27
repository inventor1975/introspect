require_relative "lib/path_scrubber"

class ExportsController < ApplicationController
  EXPORT_DIR = Rails.root.join("tmp", "exports")

  def download
    name = PathScrubber.clean(params[:name])
    path = EXPORT_DIR.join(name)
    return head(:not_found) unless path.file?

    send_file path, type: "text/csv", disposition: "attachment"
  end
end
