require_relative "lib/sql_utils"

class FileIndexController < ApplicationController
  def index
    term = SqlUtils.escape_like(params[:q])
    @files = Upload.where("filename LIKE ?", "%#{term}%")
    render json: @files
  end
end
