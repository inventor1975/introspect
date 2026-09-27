class LocaleBundlesController < ApplicationController
  def show
    available = %w[en de fr es ja]
    locale = available.include?(params[:locale]) ? params[:locale] : "en"

    bundle = File.read(Rails.root.join("public", "locales", "#{locale}.json"))
    render json: bundle
  end
end
