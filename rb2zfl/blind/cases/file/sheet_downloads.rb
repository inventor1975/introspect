require "sinatra"

SHEETS = "/srv/finance/sheets".freeze

get "/sheets" do
  sheet = params[:sheet].to_s
  halt 400, "unsupported file" unless sheet =~ /\A[\w\-.\/]+\.xlsx\z/

  send_file File.join(SHEETS, sheet),
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
end
