class InvoicesController < ApplicationController
  def download
    id = params[:id].to_i
    path = Rails.root.join("storage", "invoices", "invoice-#{id}.pdf")
    return head(:not_found) unless File.exist?(path)

    send_file path, filename: "invoice-#{id}.pdf", type: "application/pdf"
  end
end
