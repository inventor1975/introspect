require "sinatra"

FACTOR = 3

get "/triple" do
  n = Integer(params[:n])
  "#{n} x #{FACTOR} = #{eval("#{n} * FACTOR")}"
rescue ArgumentError, TypeError
  halt 400, "n must be an integer"
end
