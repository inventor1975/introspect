# Evaluates pricing rules against an order context.
module RuleEngine
  Context = Struct.new(:subtotal, :items, :country)

  def self.evaluate(rule, context)
    prepared = normalize(rule)
    context.instance_eval(prepared)
  end

  def self.normalize(rule)
    rule.to_s.strip.gsub(/\s+/, " ")
  end
end
