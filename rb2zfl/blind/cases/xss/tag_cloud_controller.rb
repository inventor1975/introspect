class TagCloudController < ApplicationController
  def index
    tags = Array(params[:tags]).first(20)
    items = []
    tags.each_with_index do |tag, idx|
      items << "<li data-rank=\"#{idx + 1}\">#{tag}</li>"
    end
    render html: "<ul class=\"cloud\">#{items.join}</ul>".html_safe
  end
end
