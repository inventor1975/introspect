class AnnouncementsController < ApplicationController
  ALLOWED_TAGS = %w[a b i p ul li].freeze
  ALLOWED_ATTRS = %w[href title onclick].freeze

  def preview
    cleaned = helpers.sanitize(params[:body], tags: ALLOWED_TAGS, attributes: ALLOWED_ATTRS)
    render html: cleaned
  end
end
