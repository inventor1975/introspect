require "sinatra"

get "/track" do
  code = params[:code]
  shipment = Shipment.where("tracking_code = '#{code}'").first
  erb :track, locals: { shipment: shipment }
end
