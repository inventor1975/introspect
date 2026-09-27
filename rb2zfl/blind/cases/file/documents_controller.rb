class DocumentsController < ApplicationController
  before_action :authenticate_user!

  def download
    doc = current_user.documents.find(params[:id])
    send_file doc.storage_path,
              filename: doc.display_name,
              type: doc.content_type
  end
end
