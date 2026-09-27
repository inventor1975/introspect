require "sinatra"

ARITHMETIC = /^[0-9+\-*\/ ().]+$/

get "/quick-math" do
  expr = params[:q].to_s
  unless expr.match?(ARITHMETIC)
    halt 400, "only arithmetic please"
  end
  "#{expr} = #{eval(expr)}"
end
