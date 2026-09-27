# Fragment builders reused by reporting endpoints.
module ReportQueries
  module_function

  # Builds a raw WHERE fragment by interpolation; preserves whatever it is given.
  def status_fragment(status)
    "status = '#{status}'"
  end

  # Returns a bind array suitable for AR's array condition form.
  def status_binding(status)
    ["status = ?", status]
  end

  def whitelist_bucket(bucket)
    { "new" => "created_at > NOW() - INTERVAL 7 DAY",
      "old" => "created_at < NOW() - INTERVAL 30 DAY" }.fetch(bucket, "1=1")
  end
end
