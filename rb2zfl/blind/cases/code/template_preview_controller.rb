require "erb"

class EmailTemplatesController < ApplicationController
  def preview
    @customer = Customer.first
    template = ERB.new(params[:template], trim_mode: "-")
    body = template.result(binding)
    render html: body.html_safe
  end
end
