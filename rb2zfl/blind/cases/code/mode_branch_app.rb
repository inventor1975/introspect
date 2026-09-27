require "sinatra"

get "/score" do
  base = params[:base].to_i
  if params[:mode] == "advanced"
    expression = params[:formula]
  else
    expression = "#{Integer(params[:bonus] || 0)} + base"
  end
  "score=#{eval(expression)}"
end
