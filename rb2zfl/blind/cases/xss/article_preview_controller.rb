class ArticlePreviewController < ApplicationController
  def show
    content = params[:content].to_s
    if params[:mode] == 'rich'
      body = content
    else
      body = ERB::Util.html_escape(content)
    end
    render html: "<article>#{body}</article>".html_safe
  end
end
