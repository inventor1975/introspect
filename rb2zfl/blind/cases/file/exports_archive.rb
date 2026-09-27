require "sinatra"

EXPORT_ROOT = "/srv/app".freeze

delete "/exports" do
  relative = "exports/%s" % params[:name]
  path = File.join(EXPORT_ROOT, relative)

  if File.exist?(path)
    File.delete(path)
    status 204
  else
    halt 404
  end
end
