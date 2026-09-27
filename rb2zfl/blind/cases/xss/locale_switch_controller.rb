class LocaleSwitchController < ApplicationController
  def banner
    lang = params[:lang].to_s
    if lang == 'de' || lang == 'fr' || lang == 'en'
      render html: "<p lang=\"#{lang}\">Language set to #{lang.upcase}</p>".html_safe
    else
      render html: '<p>Unsupported language</p>'.html_safe
    end
  end
end
