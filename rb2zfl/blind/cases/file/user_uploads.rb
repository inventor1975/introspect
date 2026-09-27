require "sinatra"

UPLOAD_ROOT = File.expand_path("/srv/uploads").freeze

get "/uploads" do
  requested = params[:path].to_s
  path = File.expand_path(requested, UPLOAD_ROOT)
  halt 403, "forbidden" unless path.start_with?(UPLOAD_ROOT + File::SEPARATOR)
  halt 404 unless File.file?(path)

  send_file path
end
