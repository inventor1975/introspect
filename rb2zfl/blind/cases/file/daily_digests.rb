require "sinatra"
require "date"

DIGEST_DIR = "/srv/digests".freeze

get "/digests" do
  day =
    begin
      Date.iso8601(params[:day].to_s)
    rescue ArgumentError
      halt 400, "bad date"
    end

  File.read(File.join(DIGEST_DIR, "#{day.strftime('%Y-%m-%d')}.html"))
end
