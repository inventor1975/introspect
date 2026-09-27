require "sinatra"
require "logger"

LOG = Logger.new($stdout)
SUMMARY_EXPRESSION = "orders.sum / [orders.size, 1].max".freeze

get "/summary" do
  orders = params[:orders].to_s.split(",").map(&:to_i)
  if params[:verbose]
    LOG.info("summary requested with expression hint: #{params[:expression]}")
  end
  "average=#{eval(SUMMARY_EXPRESSION)}"
end
