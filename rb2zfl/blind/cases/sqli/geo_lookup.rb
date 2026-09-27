require "sinatra"
require "sequel"

DB = Sequel.connect(ENV["DATABASE_URL"])

get "/geo/lookup" do
  city = params[:city]
  rows = DB["SELECT lat, lng FROM places WHERE city = '#{city}'"].all
  rows.to_json
end
