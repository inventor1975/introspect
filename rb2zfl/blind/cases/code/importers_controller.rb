class ImportersController < ApplicationController
  def create
    importer_class = params[:importer].constantize
    importer = importer_class.new(params[:source])
    summary = importer.respond_to?(:run) ? importer.run : importer.to_s
    render json: { importer: importer_class.name, summary: summary }
  end
end
