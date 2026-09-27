class SwatchesController < ApplicationController
  PALETTE = %w[red green blue amber slate].freeze

  def show
    color = params[:color]
    if PALETTE.include?(color)
      render html: "<div class=\"swatch swatch-#{color}\">#{color.capitalize}</div>".html_safe
    else
      render html: '<div class="swatch">Unknown colour</div>'.html_safe, status: :not_found
    end
  end
end
