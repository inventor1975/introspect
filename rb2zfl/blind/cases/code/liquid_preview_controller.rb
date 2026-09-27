require "liquid"

class StorefrontThemesController < ApplicationController
  def preview
    template = Liquid::Template.parse(params[:template], error_mode: :strict)
    html = template.render("shop" => { "name" => current_shop.name }, "products" => sample_products)
    render html: html
  end

  private

  def sample_products
    current_shop.products.limit(4).map { |p| { "title" => p.title, "price" => p.price.to_s } }
  end
end
