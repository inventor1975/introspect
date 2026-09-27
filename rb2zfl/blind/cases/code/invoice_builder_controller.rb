class InvoiceDocument
  def initialize
    @lines = []
  end

  def heading(text)
    @lines << "# #{text}"
  end

  def note(text)
    @lines << text
  end

  def to_s
    @lines.join("\n")
  end
end

class InvoicePreviewsController < ApplicationController
  def show
    title = params[:title].to_s.truncate(80)
    memo = params[:memo].to_s
    document = InvoiceDocument.new
    document.instance_eval do
      heading title
      note memo
    end
    render plain: document.to_s
  end
end
