class ReportBuilder
  attr_reader :columns, :filters

  def initialize
    @columns = []
    @filters = {}
  end

  def column(name, label = nil)
    @columns << { name: name, label: label || name.to_s.humanize }
  end

  def filter(field, value)
    @filters[field] = value
  end
end

class ReportDefinitionsController < ApplicationController
  before_action :authenticate_user!

  def preview
    builder = ReportBuilder.new
    builder.instance_eval(params[:definition])
    render json: { columns: builder.columns, filters: builder.filters }
  rescue SyntaxError, NameError => e
    render json: { error: e.message }, status: :unprocessable_entity
  end
end
