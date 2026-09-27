class ExportFormatsController < ApplicationController
  EXPORTERS = {
    "csv"  => "text/csv",
    "json" => "application/json",
    "xml"  => "application/xml"
  }.freeze

  def template
    fmt = params[:format_name].to_s
    return head(:bad_request) unless EXPORTERS.key?(fmt)

    source = File.read(Rails.root.join("app", "export_templates", "#{fmt}.erb"))
    render plain: source, content_type: EXPORTERS[fmt]
  end
end
