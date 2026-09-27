require_relative "lib/discount_rule"

class DiscountCodesController < ApplicationController
  RULES = {
    "SPRING10" => DiscountRule.new("SPRING10", "amount * 0.9"),
    "FLAT5"    => DiscountRule.new("FLAT5", "amount - 5")
  }.freeze

  def quote
    rule = RULES.fetch(params[:code]) { return head(:not_found) }
    render json: { total: rule.apply(params[:amount]) }
  end
end
