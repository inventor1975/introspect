require_relative "lib/formula_presets"

class MarginReportsController < ApplicationController
  def show
    revenue = params[:revenue].to_f
    cost = params[:cost].to_f
    units = params[:units].to_i
    formula = FormulaPresets.lookup(params[:formula])
    render json: { formula: params[:formula], value: eval(formula) }
  end
end
