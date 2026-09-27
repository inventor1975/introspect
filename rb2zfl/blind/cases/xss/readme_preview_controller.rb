require 'redcarpet'

class ReadmePreviewController < ApplicationController
  RENDERER = Redcarpet::Markdown.new(
    Redcarpet::Render::HTML.new(escape_html: true),
    autolink: true, tables: true
  )

  def preview
    render html: RENDERER.render(params[:markdown].to_s).html_safe
  end
end
