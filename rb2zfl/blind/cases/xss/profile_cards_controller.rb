class ProfileCard
  def initialize(display_name, role)
    @display_name = display_name
    @role = role
  end

  def to_html
    "<div class=\"card\"><strong>#{@display_name}</strong> <em>#{@role}</em></div>".html_safe
  end
end

class ProfileCardsController < ApplicationController
  def show
    card = ProfileCard.new(params[:display_name], 'member')
    render html: card.to_html
  end
end
