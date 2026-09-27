require 'date'

class ScheduleController < ApplicationController
  def day
    date = Date.iso8601(params[:date].to_s)
    render html: "<h2>Agenda for #{date.strftime('%A %d %B')}</h2>".html_safe
  rescue ArgumentError
    render html: "<p class=\"error\">Could not read the date \"#{params[:date]}\".</p>".html_safe,
           status: :unprocessable_entity
  end
end
