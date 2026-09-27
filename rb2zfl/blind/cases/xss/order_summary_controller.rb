class OrderSummaryController < ApplicationController
  def show
    summary = {
      title: params[:title],
      quantity: params[:quantity].to_i,
      note: 'Ships in 2 days'
    }
    rows = summary.map { |key, value| "<tr><th>#{key}</th><td>#{value}</td></tr>" }
    render html: "<table class=\"summary\">#{rows.join}</table>".html_safe
  end
end
