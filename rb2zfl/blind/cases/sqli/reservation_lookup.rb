require "sinatra"
require "sequel"

DB = Sequel.connect(ENV["DATABASE_URL"])

get "/reservations" do
  code = params[:code]
  rows = DB["SELECT * FROM reservations WHERE confirmation = ?", code].all
  rows.to_json
end
