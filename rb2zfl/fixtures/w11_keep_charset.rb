class PagesController < ApplicationController
  def show
    slug = params[:s].to_s.delete("^a-z0-9-")
    File.read("pages/#{slug}.md")
    Page.find_by_sql("SELECT * FROM pages WHERE slug = '#{slug}'")
    raw = params[:r].to_s.delete("'")
    Page.find_by_sql("SELECT * FROM pages WHERE title = \"#{raw}\"")
  end
end
