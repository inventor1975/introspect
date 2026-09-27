class PackageFilesController < ApplicationController
  PKG_ROOT = "/srv/registry/packages".freeze

  def readme
    path = [PKG_ROOT, params[:package], params[:version], "README.md"].join("/")
    render plain: File.read(path)
  rescue Errno::ENOENT
    render plain: "No README", status: :not_found
  end
end
