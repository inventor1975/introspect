class ArchivePagesController < ApplicationController
  PER_PAGE = 25

  def index
    page = params[:page].to_i
    page = 1 if page < 1
    offset = (page - 1) * PER_PAGE
    nav = "<nav data-offset=\"#{offset}\">Page #{page} &middot; <a href=\"?page=#{page + 1}\">Next</a></nav>"
    render html: nav.html_safe
  end
end
