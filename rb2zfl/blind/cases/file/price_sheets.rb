require "sinatra"

SHEET_DIR = "/srv/pricing".freeze

get "/prices" do
  file = params[:detail] == "1" ? "prices_full.csv" : "prices_summary.csv"
  attachment "prices-#{params[:region]}.csv"
  send_file File.join(SHEET_DIR, file), type: "text/csv"
end
