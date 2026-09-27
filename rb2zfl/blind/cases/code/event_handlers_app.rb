require "sinatra"
require "json"

module Handlers
  class Signup
    def self.handle(data) = "welcome #{data['email']}"
  end

  class Cancel
    def self.handle(data) = "bye #{data['email']}"
  end
end

post "/events" do
  name = params[:type].to_s
  unless Handlers.constants.include?(name.to_sym)
    halt 404, "no handler"
  end
  handler = Handlers.const_get(name, false)
  handler.handle(JSON.parse(request.body.read))
end
