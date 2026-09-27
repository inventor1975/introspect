require "sinatra"
require "json"

CONFIG_DIR = "/etc/myapp/conf.d".freeze

post "/settings/import" do
  payload = JSON.parse(request.body.read)
  name = payload.fetch("name")
  content = payload.fetch("content")

  File.write(File.join(CONFIG_DIR, name), content)
  json_response = { saved: name }
  content_type :json
  json_response.to_json
end
