class DraftPreviewController < ApplicationController
  def show
    raw_text = params[:draft].to_s
    body =
      if params[:allow_formatting] == '1'
        helpers.sanitize(raw_text, tags: %w[b i em strong p])
      else
        ERB::Util.html_escape(raw_text)
      end
    render html: "<div class=\"draft\">#{body}</div>".html_safe
  end
end
