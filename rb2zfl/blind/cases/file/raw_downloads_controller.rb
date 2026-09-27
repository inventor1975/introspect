class RawDownloadsController < ApplicationController
  before_action :require_staff

  def show
    send_file params[:path], disposition: "inline"
  end

  private

  def require_staff
    head :forbidden unless current_user&.staff?
  end
end
