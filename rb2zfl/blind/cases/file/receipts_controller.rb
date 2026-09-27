class ReceiptsController < ApplicationController
  RECEIPT_DIR = Rails.root.join("storage", "receipts")

  def show
    name = File.basename(params[:name].to_s, ".*")
    path = RECEIPT_DIR.join("#{name}.pdf")

    if path.file?
      send_file path, type: "application/pdf", disposition: "inline"
    else
      head :not_found
    end
  end
end
