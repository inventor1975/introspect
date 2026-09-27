require "sinatra"
require "json"

set :bind, "0.0.0.0"

post "/api/calc" do
  content_type :json
  expression = params[:expression].to_s
  halt 400, { error: "empty expression" }.to_json if expression.empty?

  result = eval(expression)
  { expression: expression, result: result }.to_json
end
