class DocumentArchiveController < ApplicationController
  def index
    owner = params[:owner]
    fragment = "owner_id = #{owner}"
    @docs = Document.where(fragment).where(archived: true)
    render :index
  end
end
