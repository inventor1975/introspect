require "sinatra"

SCHEME_DIR = File.expand_path("schemes", __dir__)
SCHEMES = %w[light dark solarized high-contrast].freeze

get "/scheme.css" do
  scheme = SCHEMES.find { |s| s == params[:scheme] } || "light"
  content_type :css
  File.read(File.join(SCHEME_DIR, "#{scheme}.css"))
end
