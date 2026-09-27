class AlertsController < ApplicationController
  include ActionView::Helpers::JavaScriptHelper

  def show
    text = escape_javascript(params[:text].to_s)
    render html: "<div class=\"alert\" role=\"alert\">#{text}</div>".html_safe
  end
end
