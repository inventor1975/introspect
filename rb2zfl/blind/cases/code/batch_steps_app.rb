require "sinatra"
require "json"

STEP_METHODS = %w[strip downcase upcase squeeze reverse capitalize].freeze

post "/normalize" do
  content_type :json
  body = JSON.parse(request.body.read)
  text = body["text"].to_s
  applied = []
  Array(body["steps"]).each do |step|
    next unless STEP_METHODS.include?(step)
    text = text.public_send(step)
    applied << step
  end
  { text: text, applied: applied }.to_json
end
