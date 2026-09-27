require "sinatra"
require "json"

class Arithmetic
  def add(a, b) = a + b
  def subtract(a, b) = a - b
  def multiply(a, b) = a * b
end

OPERATIONS = %w[add subtract multiply].freeze

post "/arith" do
  content_type :json
  op = params[:op]
  a = params[:a].to_f
  b = params[:b].to_f
  if OPERATIONS.include?(op)
    { result: Arithmetic.new.public_send(op, a, b) }.to_json
  else
    halt 400, { error: "unsupported operation" }.to_json
  end
end
