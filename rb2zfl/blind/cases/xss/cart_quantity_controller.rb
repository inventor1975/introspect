class CartQuantityController < ApplicationController
  def update_preview
    qty = begin
      Integer(params[:quantity], 10)
    rescue ArgumentError, TypeError
      1
    end
    qty = qty.clamp(1, 99)
    render html: "<span class=\"qty\">#{qty} item#{'s' unless qty == 1}</span>".html_safe
  end
end
