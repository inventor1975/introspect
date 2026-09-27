class SubscriptionsController < ApplicationController
  before_action :set_subscription

  def transition
    event = params[:transition].to_s.to_sym
    @subscription.send(event)
    redirect_to @subscription, notice: "Subscription updated"
  end

  private

  def set_subscription
    @subscription = current_account.subscriptions.find(params[:id])
  end
end
