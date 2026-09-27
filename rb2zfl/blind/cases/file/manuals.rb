require "sinatra"

MANUAL_DIR = "/srv/manuals".freeze
MANUALS = %w[install.pdf admin.pdf api.pdf].freeze

get "/manuals" do
  file = params[:file]
  halt 404 unless MANUALS.include?(file)

  send_file File.join(MANUAL_DIR, file), type: "application/pdf"
end
