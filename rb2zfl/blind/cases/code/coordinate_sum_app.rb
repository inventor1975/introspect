require "sinatra"

get "/distance" do
  dx = params[:x].to_i
  dy = params[:y].to_i
  code = "Math.sqrt(#{dx}**2 + #{dy}**2)"
  eval(code).round(3).to_s
end
