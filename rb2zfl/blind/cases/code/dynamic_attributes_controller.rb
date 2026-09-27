class Widget
  def initialize(data)
    @data = data
  end
end

class WidgetFieldsController < ApplicationController
  def create
    attribute = params[:attribute]
    Widget.class_eval("def #{attribute}; @data['#{attribute}']; end")
    widget = Widget.new(params.fetch(:data, {}).to_unsafe_h)
    render json: { attribute => widget.public_send(attribute) }
  end
end
