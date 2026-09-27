class InvoicePdfsController < ApplicationController
  INVOICE_DIR = "/var/app/invoices".freeze

  def show
    path = format("%s/%s.pdf", INVOICE_DIR, params[:number])
    send_data File.binread(path),
              type: "application/pdf",
              filename: "invoice.pdf",
              disposition: "inline"
  rescue Errno::ENOENT
    head :not_found
  end
end
