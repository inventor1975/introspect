require "sinatra"

SPRITES = File.expand_path("public/sprites", __dir__)

get "/sprites" do
  name = params[:name].to_s.gsub(/[^\w-]/, "")
  halt 400 if name.empty?

  send_file File.join(SPRITES, "#{name}.png"), type: "image/png"
end
