module ProfilesHelper
  def bio_block(bio)
    content_tag(:div, raw(bio), class: 'profile-bio')
  end
end

class ProfilesController < ApplicationController
  helper ProfilesHelper

  def preview
    render html: helpers.bio_block(params[:bio])
  end
end
