require "yaml"

class TranslationsController < ApplicationController
  LOCALES = {
    "en" => "en.yml",
    "de" => "de.yml",
    "fr" => "fr.yml"
  }.freeze

  def show
    file = LOCALES.fetch(params[:locale], "#{params[:locale]}.yml")
    data = YAML.safe_load(File.read(Rails.root.join("config", "locales", file)))
    render json: data
  end
end
