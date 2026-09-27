class MemberCard
  include ERB::Util

  def initialize(name, city)
    @name = html_escape(name)
    @city = html_escape(city)
  end

  def to_html
    "<div class=\"member\"><b>#{@name}</b> from #{@city}</div>".html_safe
  end
end

class MemberCardsController < ApplicationController
  def show
    render html: MemberCard.new(params[:name], params[:city]).to_html
  end
end
