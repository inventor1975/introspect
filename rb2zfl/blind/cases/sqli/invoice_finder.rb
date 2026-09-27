class InvoicesController < ApplicationController
  def find
    number = params[:number]
    @invoice = Invoice.where("invoice_number = " + number).first
    render json: @invoice
  end
end
