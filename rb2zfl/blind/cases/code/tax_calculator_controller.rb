class TaxCalculatorController < ApplicationController
  def show
    value = parse_amount(params[:amount])
    return render(json: { error: "invalid amount" }, status: :unprocessable_entity) if value.nil?

    rate = TaxRate.for_region(params[:region]).to_f
    render json: { gross: eval("#{value} * (1 + #{rate})").round(2) }
  end

  private

  def parse_amount(raw)
    Float(raw)
  rescue ArgumentError, TypeError
    nil
  end
end
