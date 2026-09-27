require "pathname"

class WikiPagesController < ApplicationController
  WIKI_ROOT = Pathname.new("/srv/wiki/pages")

  def show
    target = WIKI_ROOT.join(params[:page].to_s).cleanpath
    unless target.to_s.start_with?("#{WIKI_ROOT}/")
      head :forbidden
      return
    end

    @body = File.read(target)
    render :show
  rescue Errno::ENOENT
    head :not_found
  end
end
