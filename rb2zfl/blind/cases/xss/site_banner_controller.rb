require 'yaml'

class SiteBannerController < ApplicationController
  BANNER_FILE = Rails.root.join('config', 'banner.yml')

  def show
    config = YAML.safe_load(File.read(BANNER_FILE))
    ref = ERB::Util.h(params[:ref])
    render html: "<div class=\"site-banner\">#{config['message_html']}</div><small>via #{ref}</small>".html_safe
  end
end
