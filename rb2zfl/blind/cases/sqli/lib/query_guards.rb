# Shared query-building guards used across several endpoints.
module QueryGuards
  SORT_COLUMNS = %w[name email created_at updated_at id price].freeze
  ORDER_DIRECTIONS = %w[asc desc].freeze

  module_function

  def safe_sort(value, default = "id")
    SORT_COLUMNS.include?(value.to_s) ? value.to_s : default
  end

  def safe_direction(value)
    ORDER_DIRECTIONS.include?(value.to_s.downcase) ? value.to_s.downcase : "asc"
  end

  def numeric_id(value)
    Integer(value)
  rescue ArgumentError, TypeError
    0
  end
end
