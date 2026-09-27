class Exporter
  def self.formats
    descendants.map(&:name)
  end
end

class CsvExporter < Exporter; end
class JsonExporter < Exporter; end

class DataExportsController < ApplicationController
  def create
    name = params[:exporter].to_s
    unless Exporter.formats.include?(name)
      return render(json: { error: "unknown exporter" }, status: :unprocessable_entity)
    end
    exporter = name.constantize.new
    send_data exporter.export(current_account), filename: "export"
  end
end
