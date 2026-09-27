class Admin::BulkActionsController < ApplicationController
  def perform
    operation = params[:operation]
    arguments = Array(params[:args])
    results = {}

    Invoice.where(id: params[:ids]).find_each do |invoice|
      results[invoice.id] = invoice.send(operation, *arguments)
    end

    render json: { operation: operation, results: results }
  end
end
