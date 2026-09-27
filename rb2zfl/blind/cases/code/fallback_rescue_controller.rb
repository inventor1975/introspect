class MeasurementsController < ApplicationController
  def convert
    raw = params[:value].to_s
    value = parse_value(raw)
    render json: { centimeters: value * 2.54 }
  end

  private

  def parse_value(raw)
    Float(raw)
  rescue ArgumentError
    # older clients send fractions like "3 + 1/2"
    eval(raw).to_f
  end
end
