class SubscriptionReportController < ApplicationController
  def index
    plan = params[:plan]
    @subs = Subscription.where("plan_code = '#{plan}'")
                        .group("billing_cycle")
                        .having("COUNT(*) > #{params[:min]}")
    render json: @subs.count
  end
end
