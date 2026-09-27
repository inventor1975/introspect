require 'redcarpet'

class HelpDocsPreviewController < ApplicationController
  def preview
    renderer = Redcarpet::Render::HTML.new(filter_html: true, escape_html: true, safe_links_only: true)
    html = Redcarpet::Markdown.new(renderer, autolink: true).render(params[:source].to_s)
    render html: html.html_safe
  end
end
