require "sinatra"

CLIPS = "/srv/audio/clips".freeze

get "/clips" do
  file =
    case params[:clip]
    when "chime" then "chime.ogg"
    when "alert" then "alert.ogg"
    when "done"  then "done.ogg"
    else halt 404
    end

  send_file File.join(CLIPS, file), type: "audio/ogg"
end
