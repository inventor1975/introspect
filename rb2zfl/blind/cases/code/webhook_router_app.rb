require "sinatra"
require "json"

ACTIONS = {
  "push" => :handle_push,
  "pull_request" => :handle_pull_request,
  "ping" => :handle_ping
}.freeze

helpers do
  def handle_push(payload) = "push to #{payload['ref']}"
  def handle_pull_request(payload) = "pr ##{payload['number']}"
  def handle_ping(_payload) = "pong"
end

post "/webhooks" do
  event = request.env["HTTP_X_GITHUB_EVENT"].to_s
  halt 202, "ignored" unless ACTIONS.key?(event)
  payload = JSON.parse(request.body.read)
  method(ACTIONS[event]).call(payload)
end
