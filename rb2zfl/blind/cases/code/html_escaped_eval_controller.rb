class GradeCalculatorController < ApplicationController
  include ERB::Util

  def compute
    weights = html_escape(params[:weights])
    total = eval("[#{weights}].sum")
    render json: { total: total }
  end
end
