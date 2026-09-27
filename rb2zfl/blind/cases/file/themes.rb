require "sinatra"
require "sinatra/cookies"

get "/theme.css" do
  theme = cookies[:theme] || "default"
  content_type :css
  File.read("themes/#{theme}.css")
end
