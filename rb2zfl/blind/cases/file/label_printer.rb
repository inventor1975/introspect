require "sinatra"

LABEL_DIR = "/srv/labels".freeze

get "/labels/raw" do
  name = params[:name].to_s
  halt 400, "invalid label" unless name =~ /\A[a-z0-9_-]+\z/

  content_type "text/plain"
  File.read(File.join(LABEL_DIR, "#{name}.zpl"))
end
