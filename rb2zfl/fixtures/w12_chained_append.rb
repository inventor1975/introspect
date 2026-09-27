class NotesController < ApplicationController
  def show
    out = +""
    out << "<p>" << params[:note].to_s << "</p>"
    render html: out.html_safe
  end
end
