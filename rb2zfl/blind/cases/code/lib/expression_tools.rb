# Utilities used by the analytics endpoints.
module ExpressionTools
  DEFAULT_EXPRESSION = "values.sum / [values.size, 1].max.to_f".freeze

  def self.evaluate(expression, values)
    eval(expression)
  end

  def self.describe(expression)
    tokens = expression.to_s.scan(/[A-Za-z_]+|\d+|[^\s\w]/)
    { length: expression.to_s.length, tokens: tokens.size, operators: tokens.grep(/[^\w]/).uniq }
  end
end
