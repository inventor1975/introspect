class NotificationsController < ApplicationController
  def deliver
    klass = params[:kind].to_s.safe_constantize
    return head(:bad_request) if klass.nil?

    notification = klass.new(params[:payload])
    notification.deliver_later if notification.respond_to?(:deliver_later)
    head :accepted
  end
end
