require "sinatra"
require "cgi"

PAGES_DIR = File.expand_path("pages", __dir__)

get "/page" do
  requested = params[:p].to_s
  halt 400, "bad path" if requested.include?("..")

  path = File.join(PAGES_DIR, CGI.unescape(requested))
  halt 404 unless File.exist?(path)

  File.read(path)
end
