# A discount rule stores a Ruby-ish expression template such as "amount * 0.9".
class DiscountRule
  attr_reader :code, :template

  def initialize(code, template)
    @code = code
    @template = template
  end

  def apply(amount)
    expression = template.gsub("amount", amount.to_s)
    eval(expression)
  end
end
