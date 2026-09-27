require "sinatra"
require "json"

module Plugins
  class Echo
    def self.call(payload)
      payload
    end
  end
end

post "/plugins/invoke" do
  content_type :json
  target = Object.const_get(params[:plugin])
  entry = params[:entry] || "call"
  result = target.public_send(entry, params[:payload])
  { result: result }.to_json
end
