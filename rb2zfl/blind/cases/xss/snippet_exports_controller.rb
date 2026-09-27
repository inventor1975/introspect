class SnippetExportsController < ApplicationController
  def show
    snippet = params[:snippet].to_s
    case params[:format_hint]
    when 'html'
      output = snippet
    when 'code'
      output = "<pre>#{ERB::Util.html_escape(snippet)}</pre>"
    else
      output = ERB::Util.html_escape(snippet)
    end
    render html: output.html_safe
  end
end
