class EmbedConfigController < ApplicationController
  def show
    settings = { locale: params[:locale].to_s, referrer: params[:ref].to_s }
    payload = ERB::Util.json_escape(settings.to_json)
    render html: "<script>window.embedConfig = #{payload};</script><div id=\"embed\"></div>".html_safe
  end
end
