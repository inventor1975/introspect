require "sinatra"
require "pathname"

DOCS = Pathname.new("/srv/app/docs")

get "/preview" do
  page = params.fetch("page", "index.md")
  content_type "text/markdown"
  DOCS.join(page).read
end
