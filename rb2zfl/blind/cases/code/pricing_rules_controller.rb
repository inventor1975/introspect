require_relative "lib/rule_engine"

class PricingRulesController < ApplicationController
  def simulate
    context = RuleEngine::Context.new(
      params[:subtotal].to_f,
      params[:items].to_i,
      params[:country].to_s
    )
    rule = params.require(:rule)
    price = RuleEngine.evaluate(rule, context)
    render json: { price: price }
  end
end
