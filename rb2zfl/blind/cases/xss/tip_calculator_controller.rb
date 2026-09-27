class TipCalculatorController < ApplicationController
  def show
    bill = begin
      Float(params[:bill])
    rescue ArgumentError, TypeError
      0.0
    end
    tip = (bill * 0.15).round(2)
    render html: "<p>Bill #{bill} &rarr; suggested tip: #{helpers.number_to_currency(tip)}</p>".html_safe
  end
end
