require "yaml"

class FeatureFlagsController < ApplicationController
  def show
    config = YAML.safe_load(File.read(Rails.root.join("config", "flags.yml")))
    section = config.fetch(params[:section].to_s, {})
    render json: { section: params[:section], flags: section }
  end
end
