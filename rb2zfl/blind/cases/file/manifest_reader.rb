require "sinatra"
require "json"

MANIFEST_DIR = "/srv/app/manifests".freeze

helpers do
  def manifest_path_for(name)
    base = File.basename(name.to_s)
    halt 400, "invalid manifest" unless base.match?(/\A[\w.-]+\z/)
    File.join(MANIFEST_DIR, "#{base}.json")
  end
end

get "/manifests" do
  path = manifest_path_for(params[:name])
  halt 404 unless File.file?(path)

  content_type :json
  File.read(path)
end
