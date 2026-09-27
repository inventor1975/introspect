class InboxPreviewController < ApplicationController
  def show
    subject = params[:subject]
    body = params[:body]
    html = helpers.content_tag(:div, class: 'message') do
      helpers.content_tag(:h3, subject) + helpers.content_tag(:p, body)
    end
    render html: html
  end
end
