class ContinueLinksController < ApplicationController
  include ERB::Util

  def interstitial
    target = params[:next].to_s
    markup = <<~HTML
      <p>You are about to leave the site.</p>
      <a class="btn" href="#{html_escape(target)}">Continue</a>
    HTML
    render html: markup.html_safe
  end
end
