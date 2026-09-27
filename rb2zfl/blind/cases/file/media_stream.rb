require "sinatra"

MEDIA   = "/srv/media".freeze
POSTER  = File.join(MEDIA, "poster.jpg")
TRAILER = File.join(MEDIA, "trailer.mp4")

get "/media" do
  path =
    case params[:kind]
    when "poster" then POSTER
    when "trailer" then TRAILER
    else File.join(MEDIA, params[:kind].to_s)
    end

  send_file path
end
