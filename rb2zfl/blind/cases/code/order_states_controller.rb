class OrderStatesController < ApplicationController
  TRANSITIONS = %i[confirm ship cancel refund].freeze

  def update
    order = current_customer.orders.find(params[:order_id])
    event = params[:event].to_s.to_sym
    raise ActionController::BadRequest, "unknown event" unless TRANSITIONS.include?(event)
    order.public_send(event)
    redirect_to order_path(order)
  end
end
