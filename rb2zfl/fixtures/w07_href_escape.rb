class LinksController < ApplicationController
  def show
    u = params[:u]
    t = params[:t]
    render html: "<a href=\"#{ERB::Util.h(u)}\">go</a>".html_safe # javascript: survives escaping
    render html: "<p>#{ERB::Util.h(t)}</p>".html_safe
  end
end
