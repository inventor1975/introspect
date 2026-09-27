class ListingDescriptionsController < ApplicationController
  def preview
    text = params.dig(:listing, :description).to_s
    render html: helpers.simple_format(text, { class: 'desc' }, sanitize: false)
  end
end
