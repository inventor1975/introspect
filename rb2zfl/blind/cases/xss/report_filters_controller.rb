class ReportFiltersController < ApplicationController
  def edit
    current = ERB::Util.h(params[:filter])
    html = "<form action='/reports'><input type=text name=filter value=#{current}><button>Apply</button></form>"
    render html: html.html_safe
  end
end
