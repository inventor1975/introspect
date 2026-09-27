require 'erb'

class InvitationsController < ApplicationController
  CARD_TEMPLATE = <<~TPL
    <div class="invite">
      <p>Hi <%= guest %>, you are invited to <%= event %>.</p>
    </div>
  TPL

  def card
    html = ERB.new(CARD_TEMPLATE).result_with_hash(guest: params[:guest], event: 'the launch party')
    render html: html.html_safe
  end
end
