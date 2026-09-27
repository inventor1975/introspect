require "sinatra"

get "/round" do
  value = params["value"]
  digits = params["digits"] || "2"
  code = "%s.round(%s)" % [value, digits]
  "Rounded: #{eval(code)}"
end
