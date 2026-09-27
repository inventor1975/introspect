require_relative 'lib/escaped_snippets'

class BuildStatusController < ApplicationController
  def show
    pill = EscapedSnippets.pill(params[:label], params[:tone])
    render html: "<p>Build: #{pill}</p>".html_safe
  end
end
