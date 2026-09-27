require "sinatra"

DEFAULT_PREFS = { theme: "light", per_page: 20 }.freeze

helpers do
  def preferences
    raw = request.cookies["prefs"]
    return DEFAULT_PREFS if raw.nil? || raw.empty?
    DEFAULT_PREFS.merge(eval(raw))
  end
end

get "/settings" do
  prefs = preferences
  "theme=#{prefs[:theme]} per_page=#{prefs[:per_page]}"
end

post "/settings" do
  prefs = { theme: params[:theme], per_page: params[:per_page].to_i }
  response.set_cookie("prefs", value: prefs.inspect, path: "/")
  redirect "/settings"
end
