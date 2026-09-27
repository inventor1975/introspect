require "sinatra"

set :views, File.expand_path("views", __dir__)

get "/preview" do
  @title = "Preview"
  body_template = params[:body] || "<p>Nothing to preview</p>"
  erb body_template, layout: :layout
end
