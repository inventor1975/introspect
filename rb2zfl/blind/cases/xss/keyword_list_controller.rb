class KeywordListController < ApplicationController
  def show
    words = params[:keywords].to_s.split(',').map(&:strip).reject(&:empty?)
    list = helpers.safe_join(words.map { |w| helpers.content_tag(:li, w) })
    render html: helpers.content_tag(:ul, list, class: 'keywords')
  end
end
