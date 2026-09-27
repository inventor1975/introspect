require "sinatra"

set :root, File.dirname(__FILE__)

get "/download" do
  name = params[:name]
  halt 400, "missing name" if name.nil? || name.empty?

  path = File.join(settings.root, "files", name)
  halt 404 unless File.file?(path)

  send_file path, disposition: "attachment"
end
