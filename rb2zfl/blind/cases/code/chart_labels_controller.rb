module ChartHelper
  def axis_label(format, value)
    eval("\"#{format}\"")
  end
end

class ChartsController < ApplicationController
  include ChartHelper

  def show
    series = Sale.group_by_month(:created_at).sum(:total)
    label_format = params[:label_format] || "Month \#{value}"
    labels = series.keys.map { |value| axis_label(label_format, value) }
    render json: { labels: labels, data: series.values }
  end
end
