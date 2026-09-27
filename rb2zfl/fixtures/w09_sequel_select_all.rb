require "sinatra"

DB = Sequel.connect(ENV["DATABASE_URL"])

get "/metrics" do
  DB["SELECT * FROM metrics WHERE name = '#{params[:a]}'"].all
  ActiveRecord::Base.connection.select_all("SELECT * FROM t WHERE b = '#{params[:b]}'")
  "ok"
end
