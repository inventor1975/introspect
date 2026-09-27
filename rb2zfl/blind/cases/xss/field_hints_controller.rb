class FieldHintsController < ApplicationController
  def show
    hint = params[:hint].to_s
    render html: helpers.tag.span('?', class: 'hint', title: hint, data: { detail: hint })
  end
end
