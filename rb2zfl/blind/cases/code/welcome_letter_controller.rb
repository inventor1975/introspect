require "erb"

class WelcomeLettersController < ApplicationController
  TEMPLATE_PATH = Rails.root.join("app", "views", "letters", "welcome.txt.erb")

  def show
    template = ERB.new(File.read(TEMPLATE_PATH), trim_mode: "-")
    letter = template.result_with_hash(name: params[:name].to_s, plan: params[:plan].to_s)
    render plain: letter
  end
end
