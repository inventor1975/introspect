require "sinatra"

THUMB_DIR = "/var/cache/thumbs".freeze

get "/thumb" do
  img = params[:img].to_s
  path = File.expand_path(img, THUMB_DIR)
  halt 404 unless File.exist?(path)

  cache_control :public, max_age: 86_400
  send_file path, type: "image/png"
end
