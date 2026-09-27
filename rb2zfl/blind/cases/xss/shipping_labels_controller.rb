class ShippingLabelsController < ApplicationController
  CARRIER_NAMES = { 'ups' => 'UPS Ground', 'dhl' => 'DHL Express', 'usps' => 'USPS Priority' }.freeze

  def show
    carrier = CARRIER_NAMES.fetch(params[:carrier].to_s, 'Standard Post')
    render html: "<p>Ships with <b>#{carrier}</b></p>".html_safe
  end
end
