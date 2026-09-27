class DashboardWidgetsController < ApplicationController
  WIDGET_KINDS = %w[clock weather note].freeze

  def show
    kind = params[:kind].to_s
    return head(:not_found) unless WIDGET_KINDS.include?(kind)

    render html: send("#{kind}_widget", params[:value])
  end

  private

  def clock_widget(_value)
    '<div class="clock" data-live="1"></div>'.html_safe
  end

  def weather_widget(value)
    helpers.content_tag(:div, value, class: 'weather')
  end

  def note_widget(value)
    "<div class=\"sticky-note\">#{value}</div>".html_safe
  end
end
