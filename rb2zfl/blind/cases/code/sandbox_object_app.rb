require "sinatra"
require "json"

post "/playground" do
  content_type :json
  code = JSON.parse(request.body.read).fetch("code", "")
  sandbox = Object.new
  begin
    value = sandbox.instance_eval(code)
    { ok: true, value: value.inspect }.to_json
  rescue StandardError => e
    { ok: false, error: e.class.name }.to_json
  end
end
