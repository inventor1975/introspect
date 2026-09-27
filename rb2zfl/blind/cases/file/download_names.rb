require "sinatra"

REPORT_PATH = "/srv/reports/current.pdf".freeze

get "/report" do
  label = params[:name].to_s.strip
  label = "report" if label.empty?

  send_file REPORT_PATH,
            filename: "#{label}.pdf",
            type: "application/pdf",
            disposition: "attachment"
end
