require 'uri'

class OutboundLinksController < ApplicationController
  def interstitial
    target = params[:url].to_s
    uri = begin
      URI.parse(target)
    rescue URI::InvalidURIError
      nil
    end
    unless uri && %w[http https].include?(uri.scheme)
      return render html: '<p>Invalid link.</p>'.html_safe, status: :bad_request
    end

    link = "<a href=\"#{ERB::Util.html_escape(target)}\">Continue to #{ERB::Util.html_escape(uri.host)}</a>"
    render html: "<p>You are leaving the site.</p>#{link}".html_safe
  end
end
