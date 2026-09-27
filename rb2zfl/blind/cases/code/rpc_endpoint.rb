require "sinatra/base"
require "json"

class InventoryService
  def count(sku)
    rand(100)
  end

  def reserve(sku, qty)
    { sku: sku, reserved: qty.to_i }
  end
end

class RpcApp < Sinatra::Base
  configure do
    set :service, InventoryService.new
  end

  post "/rpc" do
    content_type :json
    method_name = params[:method]
    args = Array(params[:args])
    result = settings.service.public_send(method_name, *args)
    { id: params[:id], result: result }.to_json
  end
end
