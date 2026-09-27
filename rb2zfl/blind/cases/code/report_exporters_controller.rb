module Exports
  class CsvExporter
    def call(rows) = rows.map { |r| r.values.join(",") }.join("\n")
  end

  class XlsxExporter
    def call(rows) = rows.to_s
  end
end

class ReportExportsController < ApplicationController
  FORMATS = %w[csv xlsx].freeze

  def show
    fmt = params[:format_name].to_s.downcase
    return head(:not_acceptable) unless FORMATS.include?(fmt)
    exporter = "Exports::#{fmt.camelize}Exporter".constantize.new
    rows = Report.find(params[:id]).rows
    send_data exporter.call(rows), filename: "report.#{fmt}"
  end
end
