require 'sinatra/base'
require 'erubi'

class FeedbackBoardApp < Sinatra::Base
  set :erb, escape_html: true

  post '/feedback' do
    @comment = params[:comment]
    erb "<blockquote><%= @comment %></blockquote>"
  end
end
