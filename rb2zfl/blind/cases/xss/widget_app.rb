require 'sinatra/base'

class WidgetApp < Sinatra::Base
  helpers do
    def panel(title, body)
      "<section class=\"panel\"><h3>#{title}</h3><div>#{body}</div></section>"
    end
  end

  get '/widget' do
    content_type :html
    body panel('Your note', params[:note])
  end
end
