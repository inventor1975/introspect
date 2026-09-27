class GreetingsController < ApplicationController
  def show
    visitor = params[:name].to_s.strip
    visitor = 'friend' if visitor.empty?
    render html: "<h1>Hello, #{visitor}!</h1><p>Welcome to the member portal.</p>".html_safe
  end
end
