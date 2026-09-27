require 'sinatra/base'
require 'rack/utils'

class ShoutboxApp < Sinatra::Base
  helpers do
    def h(text)
      Rack::Utils.escape_html(text.to_s)
    end
  end

  post '/shout' do
    @shout = params[:shout]
    erb "<p class=\"shout\"><%= h @shout %></p>"
  end
end
