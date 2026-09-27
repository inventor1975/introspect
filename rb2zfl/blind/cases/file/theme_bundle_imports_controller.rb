require "zip"
require "fileutils"

class ThemeBundleImportsController < ApplicationController
  THEMES_DIR = Rails.root.join("storage", "themes").to_s

  def create
    upload = params.require(:bundle)
    dest = File.join(THEMES_DIR, current_account.id.to_s)
    FileUtils.mkdir_p(dest)

    Zip::File.open(upload.tempfile.path) do |zip|
      zip.each do |entry|
        next if entry.directory?

        target = File.join(dest, entry.name)
        FileUtils.mkdir_p(File.dirname(target))
        File.open(target, "wb") { |f| f.write(entry.get_input_stream.read) }
      end
    end

    redirect_to themes_path, notice: "Theme imported"
  end
end
