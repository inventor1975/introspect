class ExportsController < ApplicationController
  EXPORTABLE = {
    "customers" => "Customer",
    "orders"    => "Order",
    "invoices"  => "Invoice"
  }.freeze

  def create
    class_name = EXPORTABLE.fetch(params[:resource]) do
      return render(json: { error: "unknown resource" }, status: :bad_request)
    end
    model = class_name.constantize
    ExportJob.perform_later(model.name, current_user.id)
    head :accepted
  end
end
