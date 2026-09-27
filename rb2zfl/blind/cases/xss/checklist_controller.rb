class ChecklistController < ApplicationController
  def preview
    items = Array(params.fetch(:items, [])).map { |item| "<li>#{ERB::Util.h(item)}</li>" }
    render html: "<ol class=\"checklist\">#{items.join}</ol>".html_safe
  end
end
