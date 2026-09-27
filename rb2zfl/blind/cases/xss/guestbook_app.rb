require 'sinatra/base'

class GuestbookApp < Sinatra::Base
  post '/sign' do
    @signature = params[:signature]
    erb "<p>Thanks for signing the guestbook, <%= @signature %>!</p>"
  end
end
