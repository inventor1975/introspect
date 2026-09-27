# Small helpers around the AR connection.
module SqlUtils
  module_function

  def quote_literal(value)
    ActiveRecord::Base.connection.quote(value)
  end

  def escape_like(term)
    ActiveRecord::Base.sanitize_sql_like(term.to_s)
  end
end
