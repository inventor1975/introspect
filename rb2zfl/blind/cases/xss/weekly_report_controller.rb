class WeeklyReportController < ApplicationController
  def preview
    out = +'<div class="report">'
    out << '<h2>Weekly report</h2>'
    Array(params[:highlights]).each do |line|
      out << '<p>' << line.to_s.squish << '</p>'
    end
    out << '</div>'
    render html: out.html_safe
  end
end
