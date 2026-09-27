class StorefrontController < ApplicationController
  before_action :load_theme

  def home
    render html: "<body class='theme-#{@theme}'><h1>Store</h1></body>".html_safe
  end

  private

  def load_theme
    @theme = params[:theme].presence || 'light'
  end
end
