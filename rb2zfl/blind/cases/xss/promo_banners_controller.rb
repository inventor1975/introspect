class PromoBannersController < ApplicationController
  def show
    text = params[:text].to_s.truncate(80)
    render html: "<strong class=\"promo\">#{text}</strong>", layout: false
  end
end
