require "sinatra"
require "digest"
require "net/http"

CACHE_DIR = "/var/cache/api".freeze

get "/cached" do
  url = params[:url].to_s
  key = Digest::SHA256.hexdigest(url)
  path = File.join(CACHE_DIR, key)

  if File.exist?(path)
    File.read(path)
  else
    halt 404, "not cached"
  end
end
