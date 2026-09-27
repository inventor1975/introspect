class WikiPagesController < ApplicationController
  SLUG_FORMAT = /\A[a-z0-9]+(?:-[a-z0-9]+)*\z/

  def show
    slug = params[:slug].to_s
    return head(:bad_request) unless SLUG_FORMAT.match?(slug)

    render html: "<h1>#{slug.tr('-', ' ').capitalize}</h1><div id=\"page-#{slug}\"></div>".html_safe
  end
end
