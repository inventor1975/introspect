require "sinatra/base"

class Greeter < Sinatra::Base
  get "/hello" do
    "<h1>Hello #{params[:name]}</h1>"
  end
end
