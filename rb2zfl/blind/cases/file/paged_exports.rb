require "sinatra"

EXPORT_DIR = "/srv/exports/pages".freeze

get "/exports/page" do
  page =
    begin
      Integer(params[:page], 10)
    rescue ArgumentError, TypeError
      halt 400, "page must be a number"
    end

  content_type :json
  File.read(File.join(EXPORT_DIR, format("page-%04d.json", page)))
end
