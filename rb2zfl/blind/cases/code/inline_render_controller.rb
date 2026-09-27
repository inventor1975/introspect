class LandingPagesController < ApplicationController
  layout "marketing"

  def show
    headline = params[:title].presence || "Welcome"
    render inline: "<h1 class=\"hero\">#{headline}</h1><p><%= link_to 'Sign up', new_user_registration_path %></p>"
  end
end
