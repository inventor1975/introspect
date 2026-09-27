class SectionsController < ApplicationController
  def header
    heading =
      case params[:section]
      when 'news' then 'Latest News'
      when 'blog' then 'From the Blog'
      when 'jobs' then 'Careers'
      else 'Home'
      end
    render html: "<header><h1>#{heading}</h1></header>".html_safe
  end
end
