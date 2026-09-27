require "sinatra"
require "fileutils"

WORKSPACES = "/srv/builder/workspaces".freeze

post "/workspaces/purge" do
  workspace = params[:workspace].to_s
  halt 422, "workspace required" if workspace.strip.empty?

  target = File.join(WORKSPACES, workspace)
  FileUtils.rm_rf(target)
  status 204
end
