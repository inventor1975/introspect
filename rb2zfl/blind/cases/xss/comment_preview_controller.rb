class CommentPreviewController < ApplicationController
  SCRIPT_TAG = %r{<script\b[^>]*>.*?</script>}im

  def create
    text = params[:comment].to_s.gsub(SCRIPT_TAG, '')
    render html: "<div class=\"comment\">#{text}</div>".html_safe
  end
end
