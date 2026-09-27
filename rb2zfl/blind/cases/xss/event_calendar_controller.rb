require 'date'

class EventCalendarController < ApplicationController
  def day
    day = parse_day(params[:day])
    render html: "<h2>Events on #{day.strftime('%Y-%m-%d')}</h2>".html_safe
  end

  private

  def parse_day(value)
    Date.parse(value.to_s)
  rescue ArgumentError
    Date.today
  end
end
