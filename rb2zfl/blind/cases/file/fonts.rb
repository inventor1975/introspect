require "sinatra"

FONT_DIR = File.expand_path("assets/fonts", __dir__)

get "/fonts" do
  font = Dir.children(FONT_DIR).find { |f| f == params[:font] }
  halt 404 unless font

  cache_control :public, max_age: 31_536_000
  send_file File.join(FONT_DIR, font)
end
