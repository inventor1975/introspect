require "yaml"

class ShippingRulesController < ApplicationController
  RULES_FILE = Rails.root.join("config", "shipping_rules.yml")

  def quote
    rules = YAML.safe_load_file(RULES_FILE)
    rule = rules.fetch(params[:region]) { rules.fetch("default") }
    weight = params[:weight].to_f
    render json: { cost: eval(rule["formula"]) }
  end
end
