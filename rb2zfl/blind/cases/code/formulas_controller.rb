class FormulasController < ApplicationController
  before_action :set_formula

  def update
    if @formula.update(expression: params[:formula][:expression])
      redirect_to @formula
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def compute
    inputs = params.fetch(:inputs, {}).to_unsafe_h.transform_values(&:to_f)
    x = inputs["x"] || 0
    y = inputs["y"] || 0
    render json: { value: eval(@formula.expression) }
  end

  private

  def set_formula
    @formula = current_team.formulas.find(params[:id])
  end
end
