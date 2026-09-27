require "sinatra"
require "date"

REPORT_DIR = ENV.fetch("REPORT_DIR", "/var/reports")

get "/nightly" do
  since = params[:since].to_s
  lines = File.readlines(File.join(REPORT_DIR, "nightly.txt"), chomp: true)
  lines = lines.select { |l| l >= since } unless since.empty?

  content_type "text/plain"
  lines.join("\n")
end
