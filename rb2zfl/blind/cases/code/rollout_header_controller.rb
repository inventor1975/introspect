class FeatureRolloutController < ApplicationController
  skip_before_action :verify_authenticity_token

  def check
    rule = request.headers["X-Rollout-Rule"]
    user = current_user
    enabled = rule.present? ? eval(rule) : false
    render json: { enabled: !!enabled }
  end
end
