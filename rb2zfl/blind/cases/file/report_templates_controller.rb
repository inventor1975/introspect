require_relative "lib/report_template"

class ReportTemplatesController < ApplicationController
  def preview
    body = ReportTemplate.body_for(params[:template])
    render plain: body
  end
end
