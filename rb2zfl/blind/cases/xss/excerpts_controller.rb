class ExcerptsController < ApplicationController
  def preview
    excerpt = helpers.truncate(params[:text].to_s, length: 140, separator: ' ')
    render html: "<p class=\"excerpt\">#{excerpt}</p>".html_safe
  end
end
