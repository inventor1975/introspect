class HelpArticlesController < ApplicationController
  HELP_DIR = Rails.root.join("app", "help").to_s

  def show
    name = ERB::Util.html_escape(params[:article])
    html = File.read(File.join(HELP_DIR, "#{name}.html"))
    render html: html.html_safe, layout: "help"
  end
end
