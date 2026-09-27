require "sinatra"

ARITHMETIC_ONLY = /\A[\d\s+\-*\/().]{1,64}\z/

get "/quick-sum" do
  expr = params[:q].to_s
  halt 400, "only arithmetic please" unless ARITHMETIC_ONLY.match?(expr)
  "#{expr} = #{eval(expr)}"
end
