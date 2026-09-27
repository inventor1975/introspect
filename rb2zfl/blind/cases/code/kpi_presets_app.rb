require "sinatra"

PRESETS = {
  "basic"  => "visits * 1.0",
  "weighted" => "visits * 0.7 + signups * 3.0",
  "retention" => "returning / [visits, 1].max.to_f"
}.freeze

get "/kpi" do
  visits = params[:visits].to_i
  signups = params[:signups].to_i
  returning = params[:returning].to_i

  expr = params[:expr]
  logger.info("client requested custom expr #{expr.inspect}, using presets instead") if expr
  expr = PRESETS.fetch(params[:preset], PRESETS["basic"])

  "kpi=#{eval(expr)}"
end
