class MediaGalleryController < ApplicationController
  def index
    album = params[:album]
    keyword = params[:keyword]
    query = "album = '#{album}'"
    query += " AND caption LIKE '%#{keyword}%'" if keyword.present?
    @media = Media.where(query)
    render :index
  end
end
