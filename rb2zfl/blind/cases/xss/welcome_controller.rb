class WelcomeController < ApplicationController
  def index
    name = params[:name].presence || 'guest'
    render html: "<h1>Welcome, #{ERB::Util.html_escape(name)}!</h1>".html_safe
  end
end
